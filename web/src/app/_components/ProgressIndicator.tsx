import React from 'react';

interface ProgressIndicatorProps {
  startTime: Date;
}

const ProgressIndicator: React.FC<ProgressIndicatorProps> = ({ startTime }) => {
  if (!(startTime instanceof Date)) {
    console.error('ProgressIndicator: startTime must be a Date object');
    return null;
  }

  const totalEstimatedTime = 438;
  const now = new Date();
  const timeElapsed = Math.floor((now.getTime() - startTime.getTime()) / 1000);
  const progress = Math.min(100, (timeElapsed / totalEstimatedTime) * 100);
  const timeRemaining = Math.max(0, totalEstimatedTime - timeElapsed);

  return (
    <div className="mt-4">
      <div className="w-full bg-gray-200 rounded-full h-2.5" role="progressbar" aria-label="Video processing progress" aria-valuenow={Math.round(progress)} aria-valuemin={0} aria-valuemax={100}>
        <div
          className="bg-blue-600 h-2.5 rounded-full"
          style={{ width: `${progress}%` }}
        ></div>
      </div>
      {timeRemaining < 2 ? (
        <p className="mt-2">It&apos;s taking longer than usual, but your video will be completed soon.</p>
      ) : (
        <p className="mt-2">Estimated time remaining: {timeRemaining} second{timeRemaining !== 1 ? 's' : ''}</p>
      )}
    </div>
  );
};

export default ProgressIndicator;
