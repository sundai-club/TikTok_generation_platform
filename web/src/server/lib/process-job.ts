import path from "path";
import { db } from "../db";
import crypto from "crypto";
import * as childProcess from "child_process";
import fs from "fs";
import { getVideoStyleNames } from "@/lib/video-style-names";
import assert from "assert";

export async function processJob(jobId: number) {
  console.log(`Starting processJob for jobId: ${jobId}`);

  const job = await db.job.findUniqueOrThrow({
    where: { id: jobId },
  });
  console.log(`Job found: ${JSON.stringify(job.id)}`);

  await db.job.update({
    where: { id: jobId },
    data: { status: "Processing" },
  });
  console.log(`Job status updated to Processing`);

  try {
    const epubToMp4ScriptPath = "/opt/app/bin/epub-to-mp4";
    console.log(`epubToMp4ScriptPath: ${epubToMp4ScriptPath}`);

    const epubTmpPath = job.epubTmpPath;
    console.log(`epubTmpPath: ${epubTmpPath}`);

    const mp4TmpPath = path.join(
      "/tmp",
      `${crypto.randomBytes(16).toString("hex")}.mp4`,
    );
    console.log(`mp4TmpPath: ${mp4TmpPath}`);

    // call epub-to-mp4 with the epubTmpPath and mp4TmpPath async and pass the stdout/stderr to our own stdout/stderr
    await new Promise<void>((resolve, reject) => {

      // get the style name, defaulting to the first name in the list if it's not already a name in the list
      const possibleStyles = getVideoStyleNames();
      const requestedName = job.videoStyle;
      let style = possibleStyles.find((style) => style === requestedName);
      if (!style) {
        console.error(`Style ${requestedName} not found, defaulting to ${possibleStyles[0]}`);
        style = possibleStyles[0] ?? "";
        assert(style.length > 0, "Style not found");
      }

      console.log(
        `Spawning child process: ${epubToMp4ScriptPath} ${epubTmpPath} ${mp4TmpPath} ${style}`,
      );

      const process = childProcess.spawn(epubToMp4ScriptPath, [
        epubTmpPath,
        mp4TmpPath,
        style,
      ]);

      process.stdout.on("data", (data) => {
        console.log(`stdout: ${data}`);
      });

      process.stderr.on("data", (data) => {
        console.error(`stderr: ${data}`);
      });

      process.on("close", (code) => {
        console.log(`Child process closed with code: ${code}`);
        if (code === 0) {
          resolve();
        } else {
          reject(new Error(`Process exited with code ${code}`));
        }
      });
    });

    // read the mp4 file and save it into job.mp4Data
    console.log(`Reading mp4 file from: ${mp4TmpPath}`);
    const mp4Data = await fs.promises.readFile(mp4TmpPath);
    console.log(`mp4Data length: ${mp4Data.length}`);

    await db.job.update({
      where: { id: jobId },
      data: {
        mp4Data: mp4Data.toString("base64"),
        status: "Completed",
      },
    });
    console.log(`Job ${jobId} updated with mp4Data and status 'Completed'`);
  } catch (error) {
    console.error(`Failed to process job ${jobId}`);
    await db.job.update({
      where: { id: jobId },
      data: {
        status: "Failed",
      },
    });
    console.log(`Job ${jobId} updated with status 'Failed'`);
  }
}
