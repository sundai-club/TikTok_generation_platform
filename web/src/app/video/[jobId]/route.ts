import { db } from "@/server/db";
import { NextResponse } from "next/server";

export async function GET(
  request: Request,
  { params }: { params: { jobId: string } }
) {
  const jobId = params.jobId;

  try {
    const job = await db.job.findUnique({
      where: { id: parseInt(jobId, 10) },
      select: { mp4Data: true },
    });

    if (!job?.mp4Data) {
      return new NextResponse("Video not found", { status: 404 });
    }

    const videoBuffer = Buffer.from(job.mp4Data, 'base64');

    return new NextResponse(videoBuffer, {
      headers: {
        'Content-Type': 'video/mp4',
        'Content-Disposition': `inline; filename="video_${jobId}.mp4"`,
      },
    });
  } catch (error) {
    console.error("Error fetching video:", error);
    return new NextResponse("Internal Server Error", { status: 500 });
  }
}
