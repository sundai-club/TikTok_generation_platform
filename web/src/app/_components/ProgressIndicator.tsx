import React, { useState, useEffect } from 'react';

const ProgressIndicator: React.FC = () => {
  const [timeLeft, setTimeLeft] = useState(420); // 7 minutes in seconds

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft((prevTime) => {
        if (prevTime <= 0) {
          clearInterval(timer);
          return 0;
        }
        return prevTime - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const minutes = Math.floor(timeLeft / 60);
  const seconds = timeLeft % 60;
  const progress = ((420 - timeLeft) / 420) * 100;

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
