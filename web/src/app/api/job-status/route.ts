import { type NextRequest, NextResponse } from 'next/server';
import { db } from "@/server/db";

export async function GET(request: NextRequest) {
  const jobId = request.nextUrl.searchParams.get('jobId');

  if (!jobId) {
    return NextResponse.json({ error: 'No job ID provided' }, { status: 400 });
  }

  try {
    const job = await db.job.findUnique({
      where: { id: parseInt(jobId, 10) },
      select: { status: true, updatedAt: true },
    });

    if (!job) {
      return NextResponse.json({ error: 'Job not found' }, { status: 404 });
    }

    return NextResponse.json({
      status: job.status,
      updatedAt: job.updatedAt.toISOString(),
      processingStartedAt: job.status === "Processing" ? job.updatedAt.toISOString() : null,
      videoUrl: job.status === "Completed" ? `/video/${jobId}` : null,
    });
  } catch (error) {
    console.error('Error fetching job status:', error);
    return NextResponse.json({ error: 'Error fetching job status' }, { status: 500 });
  }
}
