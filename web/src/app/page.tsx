"use client";

import { useCallback, useState, useEffect } from "react";
import { useDropzone } from "react-dropzone";
import { api } from "@/trpc/react";

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

  const uploadFile = api.main.uploadFile.useMutation({
    onSuccess: (data) => {
      console.log(`File uploaded successfully. Job ID: ${data.jobId}`);
      setUploadStatus(`File uploaded successfully. Job ID: ${data.jobId}`);
      setJobId(data.jobId.toString());
    },
    onError: (error) => {
      console.log(`Error uploading file: ${error.message}`);
      setUploadStatus(`Error uploading file: ${error.message}`);
    },
  });

  const getJobStatus = api.main.getJobStatus.useQuery(
    { jobId: jobId ?? "" },
    {
      enabled: !!jobId,
      refetchInterval: 1000,
    }
  );

  useEffect(() => {
    if (getJobStatus.data) {
      setJobStatus(getJobStatus.data.status);
      if (getJobStatus.data.videoUrl) {
        setVideoUrl(getJobStatus.data.videoUrl);
      }
    }
  }, [getJobStatus.data]);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setFiles(acceptedFiles);
    acceptedFiles.forEach((file) => {
      const reader = new FileReader();
      reader.onload = () => {
        const base64String = reader.result as string | null;
        if (base64String) {
          const base64Data = base64String.split(',')[1];
          if (base64Data) {
            uploadFile.mutate({ file: base64Data });
          }
        }
      };
      reader.readAsDataURL(file);
    });
  }, [uploadFile]);

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
