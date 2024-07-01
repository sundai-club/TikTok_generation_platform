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
    const range = request.headers.get('range');

    if (range) {
      const [startStr, endStr] = range.replace(/bytes=/, "").split("-");
      const start = parseInt(startStr!, 10);
      const end = endStr ? parseInt(endStr, 10) : videoBuffer.length - 1;
      const chunkSize = (end - start) + 1;
      const videoChunk = videoBuffer.slice(start, end + 1);

      return new NextResponse(videoChunk, {
        status: 206,
        headers: {
          'Content-Range': `bytes ${start}-${end}/${videoBuffer.length}`,
          'Accept-Ranges': 'bytes',
          'Content-Length': chunkSize.toString(),
          'Content-Type': 'video/mp4',
          'Content-Disposition': `inline; filename="video_${jobId}.mp4"`,
        },
      });
    }

    return new NextResponse(videoBuffer, {
      headers: {
        'Content-Type': 'video/mp4',
        'Content-Disposition': `inline; filename="video_${jobId}.mp4"`,
        'Content-Length': videoBuffer.length.toString(),
      },
    });
  } catch (error) {
    console.error("Error fetching video:", error);
    return new NextResponse("Internal Server Error", { status: 500 });
  }
}
