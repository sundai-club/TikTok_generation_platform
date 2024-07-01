/* eslint-disable @typescript-eslint/no-unsafe-call */
/* eslint-disable @typescript-eslint/no-misused-promises */
/* eslint-disable @typescript-eslint/no-unsafe-assignment */
/* eslint-disable @typescript-eslint/no-unsafe-argument */
/* eslint-disable @typescript-eslint/no-unsafe-member-access */
"use client";

import { useCallback, useState, useEffect } from "react";
import { useDropzone } from "react-dropzone";

function VideoPlayer({ videoUrl }: { videoUrl: string }) {
  return (
    <div className="mt-8">
      <h2 className="text-2xl font-semibold mb-4">Generated Video</h2>
      <video controls width="640" height="360">
        <source src={videoUrl} type="video/mp4" />
        Your browser does not support the video tag.
      </video>
    </div>
  );
}

function FileUploader() {
  const [files, setFiles] = useState<File[]>([]);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);
  const [jobId, setJobId] = useState<string | null>(null);
  const [jobStatus, setJobStatus] = useState<string | null>(null);
  const [videoUrl, setVideoUrl] = useState<string | null>(null);

  const uploadFile = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      const data = await response.json();
      console.log(`File uploaded successfully. Job ID: ${data.jobId}`);
      setUploadStatus(`File uploaded successfully. Job ID: ${data.jobId}`);
      setJobId(data.jobId.toString());
    } catch (error) {
      console.error(`Error uploading file:`, error);
      setUploadStatus(`Error uploading file: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  };

  const getJobStatus = async () => {
    if (!jobId) return;

    try {
      const response = await fetch(`/api/job-status?jobId=${jobId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch job status');
      }
      const data = await response.json();
      setJobStatus(data.status);
      if (data.videoUrl) {
        setVideoUrl(data.videoUrl);
      }
    } catch (error) {
      console.error('Error fetching job status:', error);
    }
  };

  useEffect(() => {
    if (jobId) {
      const interval = setInterval(getJobStatus, 1000);
      return () => clearInterval(interval);
    }
  }, [jobId]);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setFiles(acceptedFiles);
    acceptedFiles.forEach((file) => {
      void uploadFile(file);
    });
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  const showUploadZone = files.length === 0;
  const showUploadedInfo = files.length > 0 && !videoUrl;

  return (
    <div>
      {showUploadZone && (
        <div {...getRootProps()} className="border-2 border-dashed border-white p-8 rounded-xl cursor-pointer">
          <input {...getInputProps()} aria-label="File upload" />
          {
            isDragActive ?
              <p>Drop the files here ...</p> :
              <p>Drag and drop some files here, or click to select files</p>
          }
        </div>
      )}
      {showUploadedInfo && (
        <>
          <div className="mt-4">
            <h4 className="text-lg font-semibold">Uploaded files:</h4>
            <ul className="list-disc list-inside">
              {files.map(file => (
                <li key={file.name}>{file.name} - {file.size} bytes</li>
              ))}
            </ul>
          </div>
          {uploadStatus && <p className="mt-4" role="status">{uploadStatus}</p>}
          {jobStatus && <p className="mt-4">Job Status: {jobStatus}</p>}
        </>
      )}
      {videoUrl && <VideoPlayer videoUrl={videoUrl} />}
    </div>
  );
}

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b from-[#2e026d] to-[#15162c] text-white">
      <div className="rounded-xl bg-white/10 p-8">
        <h1 className="text-5xl font-bold mb-8">Generate a video from an epub file</h1>
        <FileUploader />
      </div>
    </main>
  );
}
