/* eslint-disable @typescript-eslint/no-unsafe-call */
/* eslint-disable @typescript-eslint/no-misused-promises */
/* eslint-disable @typescript-eslint/no-unsafe-assignment */
/* eslint-disable @typescript-eslint/no-unsafe-argument */
/* eslint-disable @typescript-eslint/no-unsafe-member-access */
"use client";

import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";


function FileUploader() {
  const [files, setFiles] = useState<File[]>([]);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);

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
      
      // Redirect to the job page
      window.location.href = `/v/${data.jobId}`;
    } catch (error) {
      console.error(`Error uploading file:`, error);
      setUploadStatus(`Error uploading file: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  };

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setFiles(acceptedFiles);
    acceptedFiles.forEach((file) => {
      void uploadFile(file);
    });
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  const showUploadZone = files.length === 0;
  const showUploadedInfo = files.length > 0;

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
              {files.map((file: File) => (
                <li key={file.name}>{file.name} - {file.size} bytes</li>
              ))}
            </ul>
          </div>
          {uploadStatus && <p className="mt-4" role="status">{uploadStatus}</p>}
        </>
      )}
    </div>
  );
}

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b from-[#2e026d] to-[#15162c] text-white">
      <div className="rounded-xl bg-white/10 p-8">
        <h1 className="text-5xl font-bold mb-8">Generate a video from a script (a .txt file)</h1>
        <FileUploader />
      </div>
    </main>
  );
}
