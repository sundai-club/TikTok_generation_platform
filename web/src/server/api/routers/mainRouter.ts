import { z } from "zod";
import { createTRPCRouter, publicProcedure } from "@/server/api/trpc";
import { db } from "@/server/db";

export const mainRouter = createTRPCRouter({
  // Other procedures can be kept here if needed
});
