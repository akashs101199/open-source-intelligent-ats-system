import React from 'react';
import { FileText, Calendar, CheckCircle } from 'lucide-react';
import { formatDate, formatFileSize } from '../../utils/formatters';

const CandidateCard = ({ candidate }) => {
  return (
    <div className="card p-4 hover:border-purple-500 transition-colors">
      <div className="flex items-start gap-3 mb-3">
        <div className="bg-purple-900 bg-opacity-50 p-2 rounded">
          <FileText className="w-6 h-6 text-purple-400" />
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold truncate" title={candidate.name}>
            {candidate.name || 'Candidate'}
          </h3>
          <p className="text-xs text-gray-400 truncate" title={candidate.filename}>
            {candidate.filename}
          </p>
        </div>
      </div>

      <div className="space-y-2 text-xs text-gray-400">
        <p className="flex items-center gap-2">
          <Calendar className="w-3 h-3" />
          {formatDate(candidate.upload_time)}
        </p>
        {candidate.file_size_kb && <p>Size: {formatFileSize(candidate.file_size_kb * 1024)}</p>}
        <p className="flex items-center gap-1 text-green-400">
          <CheckCircle className="w-3 h-3" />
          Indexed
        </p>
      </div>
    </div>
  );
};

export default CandidateCard;
