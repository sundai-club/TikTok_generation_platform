import React from 'react';
import ProgressIndicator from './ProgressIndicator';
import VideoPlayer from './VideoPlayer';

interface JobStatusDisplayProps {
  jobStatus: string | null;
  processingStartTime: Date | null;
  jobId: string;
}

const JobStatusDisplay: React.FC<JobStatusDisplayProps> = ({ jobStatus, processingStartTime, jobId }) => {
  if (!jobStatus) return null;

  return (
    <>
      {jobStatus === 'New' && (
        <p className="mt-2">Your job is queued and will start processing soon.</p>
      )}
      {jobStatus === 'Processing' && (
        processingStartTime ? (
          <ProgressIndicator startTime={processingStartTime} />
        ) : (
          <p className="mt-2">Processing has started. Please wait...</p>
        )
      )}
      {jobStatus === 'Completed' && (
        <>
          <VideoPlayer videoUrl={`/video/${jobId}`} />
        </>
      )}
      {jobStatus === 'Failed' && (
        <p className="mt-4 text-red-500">Video generation failed. Please try again.</p>
      )}
    </>
  );
};

export default JobStatusDisplay;
