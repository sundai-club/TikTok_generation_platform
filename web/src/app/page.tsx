"use client";

import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { api } from "@/trpc/react";

function FileUploader() {
  const [files, setFiles] = useState<File[]>([]);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);

  const uploadFile = api.main.uploadFile.useMutation({
    onSuccess: (data) => {
      setUploadStatus(`File uploaded successfully. Path: ${data.filePath}`);
    },
    onError: (error) => {
      setUploadStatus(`Error uploading file: ${error.message}`);
    },
  });

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

  return (
    <div {...getRootProps()} className="border-2 border-dashed border-white p-8 rounded-xl cursor-pointer">
      <input {...getInputProps()} aria-label="File upload" />
      {
        isDragActive ?
          <p>Drop the files here ...</p> :
          <p>Drag and drop some files here, or click to select files</p>
      }
      {files.length > 0 ? (
        <div className="mt-4">
          <h4 className="text-lg font-semibold">Uploaded files:</h4>
          <ul className="list-disc list-inside">
            {files.map(file => (
              <li key={file.name}>{file.name} - {file.size} bytes</li>
            ))}
          </ul>
        </div>
      ) : (
        <p className="mt-4">No files uploaded yet.</p>
      )}
      {uploadStatus && <p className="mt-4" role="status">{uploadStatus}</p>}
    </div>
  );
}

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b from-[#2e026d] to-[#15162c] text-white">
      <div className="rounded-xl bg-white/10 p-8">
        <h1 className="text-5xl font-bold mb-8">File Uploader</h1>
        <FileUploader />
      </div>
    </main>
  );
}
