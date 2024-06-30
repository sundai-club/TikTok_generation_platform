"use client";

import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";

function FileUploader() {
  const [files, setFiles] = useState<File[]>([]);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setFiles(acceptedFiles);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  return (
    <div {...getRootProps()} className="border-2 border-dashed border-white p-8 rounded-xl cursor-pointer">
      <input {...getInputProps()} />
      {
        isDragActive ?
          <p>Drop the files here ...</p> :
          <p>Drag and drop some files here, or click to select files</p>
      }
      {files.length > 0 ? (
        <div className="mt-4">
          <h4>Uploaded files:</h4>
          <ul>
            {files.map(file => (
              <li key={file.name}>{file.name} - {file.size} bytes</li>
            ))}
          </ul>
        </div>
      ) : (
        <p className="mt-4">No files uploaded yet.</p>
      )}
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
