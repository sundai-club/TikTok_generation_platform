import { z } from "zod";
import { createTRPCRouter, publicProcedure } from "@/server/api/trpc";
import fs from "fs/promises";
import path from "path";
import crypto from "crypto";
import { db } from "@/server/db";
import { processJob } from "@/server/lib/process-job";

export const mainRouter = createTRPCRouter({
  uploadFile: publicProcedure
    .input(z.object({ file: z.string() }))
    .mutation(async ({ input }) => {
      console.log("Received file upload request");

      const buffer = Buffer.from(input.file, 'base64');
      const randomName = crypto.randomBytes(16).toString('hex');
      const filePath = path.join('/tmp', `${randomName}.epub`);

      console.log(`Generated random file name: ${randomName}`);
      console.log(`File path: ${filePath}`);

      await fs.writeFile(filePath, buffer);
      console.log(`File written to disk at: ${filePath}`);

      const newJob = await db.job.create({
        data: {
          epubData: buffer.toString('base64'),
          epubTmpPath: filePath,
          status: "New",
        },
      });

      console.log(`New job created with ID: ${newJob.id}`);

      void processJob(newJob.id);
      console.log(`Job processing started for job ID: ${newJob.id}`);

      return { 
        message: "File uploaded successfully",
        jobId: newJob.id,
      };
    }),

  getJobStatus: publicProcedure
    .input(z.object({ jobId: z.string() }))
    .query(async ({ input }) => {
      console.log(`Received request for job status with ID: ${input.jobId}`);

      const job = await db.job.findUnique({
        where: { id: parseInt(input.jobId, 10) },
        select: { status: true },
      });

      if (!job) {
        console.error(`Job not found with ID: ${input.jobId}`);
        throw new Error("Job not found");
      }

      console.log(`Job found with ID: ${input.jobId}, status: ${job.status}`);

      return {
        status: job.status,
        videoUrl: job.status === "Completed" ? `/video/${input.jobId}` : null,
      };
    }),
});
