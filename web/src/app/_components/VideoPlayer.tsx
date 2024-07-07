export default function VideoPlayer({ videoUrl }: { videoUrl: string }) {
  return (
    <div className="relative">
      <h2 className="text-2xl font-semibold mb-4">Generated Video</h2>
      <div className="absolute top-0 right-0">
        <a
          href={videoUrl}
          download="generated_video.mp4"
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Download
        </a>
      </div>
      <video controls width="640" height="360">
        <source src={videoUrl} type="video/mp4" />
        Your browser does not support the video tag.
      </video>
    </div>
  );
}
