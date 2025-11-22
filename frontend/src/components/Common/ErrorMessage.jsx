import React from 'react';
import { AlertCircle } from 'lucide-react';

const ErrorMessage = ({ message, onRetry }) => {
  return (
    <div className="card p-6 border-red-500">
      <div className="flex items-start gap-3">
        <AlertCircle className="w-6 h-6 text-red-400 flex-shrink-0 mt-1" />
        <div className="flex-1">
          <h3 className="font-semibold text-red-400 mb-2">Error</h3>
          <p className="text-gray-300">{message}</p>
          {onRetry && (
            <button
              onClick={onRetry}
              className="mt-4 text-purple-400 hover:text-purple-300 text-sm font-medium"
            >
              Try Again
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default ErrorMessage;
