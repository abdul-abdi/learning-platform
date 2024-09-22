import React from 'react';

const ProgressTracker = ({ progress }) => {
  const { completed_materials, total_materials, completion_rate } = progress;

  return (
    <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6" role="region" aria-label="Learning Progress">
      <h2 className="text-xl font-semibold mb-4">Your Learning Progress</h2>
      <div className="flex items-center">
        <div className="flex-1">
          <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded-full" role="progressbar" aria-valuenow={completion_rate} aria-valuemin="0" aria-valuemax="100">
            <div 
              className="h-4 bg-blue-600 rounded-full" 
              style={{ width: `${completion_rate}%` }}
            ></div>
          </div>
        </div>
        <span className="ml-4 text-lg font-medium">{completion_rate.toFixed(1)}%</span>
      </div>
      <p className="mt-2 text-sm text-gray-600 dark:text-gray-300">
        You've completed {completed_materials} out of {total_materials} materials.
      </p>
    </div>
  );
};

export default ProgressTracker;