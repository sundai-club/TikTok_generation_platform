import { z } from "zod";
import { createTRPCRouter, publicProcedure } from "@/server/api/trpc";
import fs from "fs/promises";
import path from "path";
import crypto from "crypto";
import { db } from "@/server/db";

export const mainRouter = createTRPCRouter({
  uploadFile: publicProcedure
    .input(z.object({ file: z.string() }))
    .mutation(async ({ input }) => {
      const buffer = Buffer.from(input.file, 'base64');
      const randomName = crypto.randomBytes(16).toString('hex');
      const filePath = path.join('/tmp', `${randomName}.epub`);

      await fs.writeFile(filePath, buffer);

      const newJob = await db.job.create({
        data: {
          epubData: buffer.toString('base64'),
          epubTmpPath: filePath,
          status: "New",
        },
      });

      console.log(`File saved to: ${filePath}`);

      return { 
        message: "File uploaded successfully",
        jobId: newJob.id,
      };
    }),
});
