import { z } from "zod";
import { createTRPCRouter, publicProcedure } from "@/server/api/trpc";
import fs from "fs";
import path from "path";
import crypto from "crypto";

export const mainRouter = createTRPCRouter({
  uploadFile: publicProcedure
    .input(z.object({ file: z.string() }))
    .mutation(({ input }) => {
      const buffer = Buffer.from(input.file, 'base64');
      const randomName = crypto.randomBytes(16).toString('hex');
      const filePath = path.join('/tmp', `${randomName}.epub`);

      fs.writeFileSync(filePath, buffer);

      console.log(`File saved to: ${filePath}`);

      return { 
        message: "File uploaded successfully",
        filePath 
      };
    }),
});
