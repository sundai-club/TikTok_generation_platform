import React, { useState, useEffect } from 'react';

interface ProgressIndicatorProps {
  startTime: Date;
}

const ProgressIndicator: React.FC<ProgressIndicatorProps> = ({ startTime }) => {
  const [timeElapsed, setTimeElapsed] = useState(0);
  const totalEstimatedTime = 420; // 7 minutes in seconds

  useEffect(() => {
    const timer = setInterval(() => {
      const now = new Date();
      const elapsed = Math.floor((now.getTime() - startTime.getTime()) / 1000);
      setTimeElapsed(elapsed);
    }, 1000);

    return () => clearInterval(timer);
  }, [startTime]);

  const timeLeft = Math.max(0, totalEstimatedTime - timeElapsed);
  const minutes = Math.floor(timeLeft / 60);
  const seconds = timeLeft % 60;
  const progress = Math.min(100, (timeElapsed / totalEstimatedTime) * 100);

  return (
    <div className="mt-4">
      <div className="mb-2">
        Estimated time remaining: {minutes}:{seconds.toString().padStart(2, '0')}
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2.5" role="progressbar" aria-label="Video processing progress" aria-valuenow={Math.round(progress)} aria-valuemin={0} aria-valuemax={100}>
        <div
          className="bg-blue-600 h-2.5 rounded-full"
          style={{ width: `${progress}%` }}
        ></div>
      </div>
    </div>
  );
};

export default ProgressIndicator;
