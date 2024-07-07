"use client";

import { useCallback, useState, useEffect } from "react";
import JobStatusDisplay from '@/app/_components/JobStatusDisplay';
import { z } from "zod";

export default function JobPage({ params }: { params: { jobId: string } }) {
  const [jobStatus, setJobStatus] = useState<string | null>(null);
  const [processingStartTime, setProcessingStartTime] = useState<Date | null>(null);
  const [error, setError] = useState<string | null>(null);

  const getJobStatus = useCallback(async () => {
    try {
      const response = await fetch(`/api/job-status?jobId=${params.jobId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch job status');
      }
      const jobStatusSchema = z.object({
        status: z.string(),
        updatedAt: z.string().optional(),
      });
      const data = jobStatusSchema.parse(await response.json());
      setJobStatus(data.status);
      if (data.status === "Processing" && data.updatedAt) {
        setProcessingStartTime(new Date(data.updatedAt));
      }
      setError(null);
    } catch (error) {
      console.error('Error fetching job status:', error);
      setError('Failed to fetch job status. Please try again later.');
    } finally {
    }
  }, [params.jobId]);

  useEffect(() => {
    void getJobStatus();
    const interval = setInterval(() => {
      void getJobStatus();
    }, 1000);
    return () => clearInterval(interval);
  }, [getJobStatus]);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b from-[#2e026d] to-[#15162c] text-white">
      <div className="rounded-xl bg-white/10 p-8">
        <h1 className="text-5xl font-bold mb-8">Video Generation Progress</h1>
        {error ? (
          <p className="text-red-500">{error}</p>
        ) : (
          <JobStatusDisplay
            jobStatus={jobStatus}
            processingStartTime={processingStartTime}
            jobId={params.jobId}
          />
        )}
      </div>
    </main>
  );
}
