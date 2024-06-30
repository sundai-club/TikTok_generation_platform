import { z } from "zod";
import { createTRPCRouter, publicProcedure } from "@/server/api/trpc";
import fs from "fs";
import path from "path";
import crypto from "crypto";

export const postRouter = createTRPCRouter({
  hello: publicProcedure
    .input(z.object({ text: z.string() }))
    .query(({ input }) => {
      return {
        greeting: `Hello ${input.text}`,
      };
    }),

  create: publicProcedure
    .input(z.object({ name: z.string().min(1) }))
    .mutation(async ({ ctx, input }) => {
      // simulate a slow db call
      await new Promise((resolve) => setTimeout(resolve, 1000));

      return ctx.db.post.create({
        data: {
          name: input.name,
        },
      });
    }),

  getLatest: publicProcedure.query(({ ctx }) => {
    return ctx.db.post.findFirst({
      orderBy: { createdAt: "desc" },
    });
  }),

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
