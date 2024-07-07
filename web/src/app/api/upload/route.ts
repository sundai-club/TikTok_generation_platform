import { type NextRequest, NextResponse } from 'next/server';
import { db } from "@/server/db";
import fs from "fs/promises";
import path from "path";
import crypto from "crypto";

export async function POST(request: NextRequest) {
  const formData = await request.formData();
  const file = formData.get('file') as File | null;
  const style = formData.get('style') as string | null;

  if (!file) {
    return NextResponse.json({ error: 'No file uploaded' }, { status: 400 });
  }

  if (!style) {
    return NextResponse.json({ error: 'No style selected' }, { status: 400 });
  }

  try {
    const buffer = Buffer.from(await file.arrayBuffer());
    const randomName = crypto.randomBytes(16).toString('hex');
    const filePath = path.join('/tmp', `${randomName}.epub`);

    await fs.writeFile(filePath, buffer);

    const newJob = await db.job.create({
      data: {
        epubData: buffer.toString('base64'),
        epubTmpPath: filePath,
        status: "New",
        videoStyle: style,
      },
    });

    return NextResponse.json({ 
      message: "File uploaded successfully",
      jobId: newJob.id,
    });
  } catch (error) {
    console.error('Error creating job:', error);
    // eslint-disable-next-line @typescript-eslint/restrict-plus-operands
    return NextResponse.json({ error: 'Error creating job: ' + error }, { status: 500 });
  }
}
