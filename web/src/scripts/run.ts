import "dotenv/config";

import { exec, spawn } from "child_process";
import crypto from "crypto";
import fs from "fs";
import { env } from "process";
import { promisify } from "util";

async function pathExists(path: string) {
  try {
    await fs.promises.stat(path);
    return true;
  } catch (err) {
    if ((err as { code: string })?.code === "ENOENT") {
      return false;
    }
    throw err;
  }
}

async function runIfFileChanged(
  filenameToCheck: string,
  checksumFilename: string,
  functionToRunIfChanged: () => Promise<void>,
  opts?: {
    functionToRunIfNotChanged?: () => Promise<void>;
  },
): Promise<void> {
  async function calculateChecksum(file: string): Promise<string> {
    return new Promise((resolve, reject) => {
      const hash = crypto.createHash("sha256");
      const stream = fs.createReadStream(file);

      stream.on("data", (data) => {
        hash.update(data);
      });

      stream.on("end", () => {
        resolve(hash.digest("hex"));
      });

      stream.on("error", (err) => {
        reject(err);
      });
    });
  }

  async function readChecksumFile(file: string): Promise<string | null> {
    if (!(await pathExists(file))) {
      return null;
    }
    if (!(await fs.promises.stat(file)).isFile()) {
      return null;
    }
    const data = await fs.promises.readFile(file, "utf-8");
    return data.trim();
  }

  async function writeChecksumFile(
    file: string,
    checksum: string,
  ): Promise<void> {
    await fs.promises.writeFile(file, checksum, "utf-8");
  }

  const currentChecksum = await calculateChecksum(filenameToCheck);
  const storedChecksum = await readChecksumFile(checksumFilename);

  if (storedChecksum === null || currentChecksum !== storedChecksum) {
    await functionToRunIfChanged();
    await writeChecksumFile(checksumFilename, currentChecksum);
  } else if (opts?.functionToRunIfNotChanged) {
    await opts.functionToRunIfNotChanged();
  }
}

(async () => {
  console.log(
    "running prisma generate & deploying migrations if schema has changed",
  );
  await runIfFileChanged(
    "prisma/schema.prisma",
    "/tmp/prisma-schema-checksum",
    async function () {
      console.log("running prisma generate");
      await promisify(exec)("npx prisma generate");

      // check if prisma/migrations directory exists and contains files or directories not starting with a dot
      if (
        (await pathExists("prisma/migrations")) &&
        (await fs.promises.stat("prisma/migrations")).isDirectory() &&
        (await fs.promises.readdir("prisma/migrations")).some(
          (file) => !file.startsWith("."),
        )
      ) {
        // migrations exist, apply them
        console.log("running prisma migrations");
        await promisify(exec)("npx prisma migrate deploy");
      } else {
        // use `prisma db push` instead
        console.log("running prisma db push");
        await promisify(exec)("npx prisma db push --accept-data-loss");
      }
    },
    {
      functionToRunIfNotChanged: async function () {
        console.log("schema has not changed");
      },
    },
  );

  if (env.NODE_ENV === "production") {
    console.log(`app.ts: building next.js app`);
    // run next build
    await promisify(exec)("npx next build");
  }

  // TODO: launch any background workers needed here

  console.log(`run.ts: launching next.js app in ${env.NODE_ENV} mode`);

  let command: string;
  let args: string[];

  if (env.NODE_ENV === "production") {
    // run next app
    command = "npx";
    args = ["next", "start", "-p", "8001"];
  } else {
    // run next app in dev mode
    command = "npx";
    args = ["next", "dev", "-p", "8001"];
  }

  // launch using spawn
  console.log(`run.ts: launching next.js app in ${env.NODE_ENV} mode`);
  console.log(`spawn(${command}, ${JSON.stringify(args)})`);
  console.log(`cwd: ${process.cwd()}`);
  const child = spawn(command, args);

  // wait for process to end
  await new Promise((resolve, reject) => {
    child.on("exit", (code) => {
      if (code === 0) {
        resolve(code);
      } else {
        reject(new Error(`child process exited with code ${code}`));
      }
    });
  });
})()
  .then(() => {
    console.log("run.ts: process ended");
    process.exit(0);
  })
  .catch((err) => {
    console.error(err);
    process.exit(1);
  });
