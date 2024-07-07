/* eslint-disable @typescript-eslint/no-unsafe-call */
/* eslint-disable @typescript-eslint/no-misused-promises */
/* eslint-disable @typescript-eslint/no-unsafe-assignment */
/* eslint-disable @typescript-eslint/no-unsafe-argument */
/* eslint-disable @typescript-eslint/no-unsafe-member-access */
"use client";

import { useCallback, useState, useEffect } from "react";
import { useDropzone } from "react-dropzone";
import { getVideoStyleNames } from "@/lib/video-style-names";

function FileUploader() {
  const [textContent, setTextContent] = useState<string>("");
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);
  const [videoStyles, setVideoStyles] = useState<string[]>([]);
  const [selectedStyle, setSelectedStyle] = useState<string>("");

  useEffect(() => {
    const styles = getVideoStyleNames();
    setVideoStyles(styles);
    const firstStyle = styles[0];
    if (!firstStyle) {
      console.error("No video styles found");
      throw new Error("No video styles found");
    }
    setSelectedStyle(firstStyle); // Set the first style as default
  }, []);

  const uploadFile = useCallback(async (fileToUpload: File | null, content: string | null) => {
    if (!fileToUpload && !content) {
      console.error("No file or text content provided");
      return;
    }

    const formData = new FormData();
    if (fileToUpload) {
      formData.append("file", fileToUpload);
    } else if (content) {
      const blob = new Blob([content], { type: 'text/plain' });
      formData.append("file", blob, "content.txt");
    }
    formData.append("style", selectedStyle);

    try {
      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Upload failed");
      }

      const data = await response.json();
      console.log(`File uploaded successfully. Job ID: ${data.jobId}`);
      setUploadStatus(`File uploaded successfully. Job ID: ${data.jobId}`);

      // Redirect to the job page
      window.location.href = `/v/${data.jobId}`;
    } catch (error) {
      console.error(`Error uploading file:`, error);
      setUploadStatus(
        `Error uploading file: ${error instanceof Error ? error.message : "Unknown error"}`,
      );
    }
  }, [selectedStyle]);

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      if (acceptedFiles.length === 0) {
        throw new Error("No file selected");
      }
      const droppedFile = acceptedFiles[0]!;
      void uploadFile(droppedFile, null);
    },
    [uploadFile],
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop, multiple: false });

  const handleTextSubmit = () => {
    if (textContent.trim()) {
      void uploadFile(null, textContent);
    } else {
      setUploadStatus("Please enter some text content before submitting.");
    }
  };

  return (
    <div>
      <div className="mb-4">
        <label
          htmlFor="videoStyle"
          className="block text-sm font-medium text-white"
        >
          Select Video Style:
        </label>
        <select
          id="videoStyle"
          value={selectedStyle}
          onChange={(e) => setSelectedStyle(e.target.value)}
          className="mt-1 block w-full rounded-md border-gray-300 py-2 pl-3 pr-10 text-base text-black focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
        >
          {videoStyles.map((style) => (
            <option key={style} value={style}>
              {style}
            </option>
          ))}
        </select>
      </div>
      <div className="block text-lg font-medium text-white mb-2">Upload a .txt file:</div>
      <div
        {...getRootProps()}
        className="cursor-pointer rounded-xl border-2 border-dashed border-white p-8 mb-4"
      >
        <input {...getInputProps()} aria-label="File upload" />
        {isDragActive ? (
          <p>Drop the file here ...</p>
        ) : (
          <p>Drag and drop a file here, or click to select a file</p>
        )}
      </div>
      <div className="mb-4">
        <label htmlFor="textContent" className="block text-lg font-medium text-white mb-2">
          Or paste your text content here:
        </label>
        <textarea
          id="textContent"
          value={textContent}
          onChange={(e) => setTextContent(e.target.value)}
          className="w-full h-32 p-2 text-black rounded-md"
          placeholder="Paste your text content here..."
        />
        <button
          onClick={handleTextSubmit}
          className="mt-2 rounded bg-blue-500 py-2 px-4 font-bold text-white hover:bg-blue-700"
        >
          Submit Text
        </button>
      </div>
      {uploadStatus && (
        <p className="mt-4" role="status">
          {uploadStatus}
        </p>
      )}
    </div>
  );
}

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b from-[#2e026d] to-[#15162c] text-white">
      <div className="rounded-xl bg-white/10 p-8">
        <h1 className="mb-8 text-5xl font-bold">
          Generate a video from a script
        </h1>
        <FileUploader />
      </div>
    </main>
  );
}
