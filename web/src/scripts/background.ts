import "dotenv/config";

import { db } from "@/server/db";
import { processJob } from "@/server/lib/process-job";

async function main() {
  while (true) {
    try {
      console.log("Checking for new jobs...");
      const job = await db.job.findFirst({
        where: {
          status: "New",
        },
      });
      if (!job) {
        // console.log("No new jobs found, waiting for 1 second...");
        await new Promise((resolve) => setTimeout(resolve, 10000));
        continue;
      }
      console.log(`New job found with ID: ${job.id}, processing...`);
      await processJob(job.id);
      console.log(`Job with ID: ${job.id} processed successfully.`);
      await new Promise((resolve) => setTimeout(resolve, 1000));
    } catch (error) {
      console.error("Error processing job:", error);
    }
  }
}

void main()
  .then(() => {
    process.exit(0);
  })
  .catch((e) => {
    console.error(e);
    process.exit(1);
  });
