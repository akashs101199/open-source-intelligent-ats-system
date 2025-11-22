import React from 'react';
import { Briefcase, Calendar, TrendingUp } from 'lucide-react';
import Button from '../Common/Button';
import { formatDate } from '../../utils/formatters';
import { EXPERIENCE_LEVELS } from '../../utils/constants';

const JobCard = ({ job, onMatch, onDelete, loading }) => {
  return (
    <div className="card p-6 hover:border-purple-500 transition-colors">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-start gap-3">
          <div className="bg-purple-900 bg-opacity-50 p-3 rounded">
            <Briefcase className="w-6 h-6 text-purple-400" />
          </div>
          <div>
            <h3 className="text-xl font-semibold mb-1">{job.title}</h3>
            <p className="text-sm text-gray-400 flex items-center gap-2">
              <Calendar className="w-4 h-4" />
              {formatDate(job.created_at)}
            </p>
          </div>
        </div>
      </div>

      <p className="text-gray-300 text-sm mb-4 line-clamp-2">{job.description}</p>

      <div className="mb-4">
        <p className="text-xs text-gray-500 mb-2">Experience Level:</p>
        <span className="px-3 py-1 bg-gray-700 rounded text-sm">
          {EXPERIENCE_LEVELS[job.experience_level] || job.experience_level}
        </span>
      </div>

      <div className="mb-4">
        <p className="text-xs text-gray-500 mb-2">Key Responsibilities:</p>
        <ul className="text-sm text-gray-300 space-y-1">
          {job.responsibilities.slice(0, 2).map((resp, idx) => (
            <li key={idx} className="flex items-start gap-2">
              <span className="text-purple-400 mt-1">•</span>
              <span className="line-clamp-1">{resp}</span>
            </li>
          ))}
          {job.responsibilities.length > 2 && (
            <li className="text-gray-500 text-xs">+{job.responsibilities.length - 2} more</li>
          )}
        </ul>
      </div>

      <div className="mb-6">
        <p className="text-xs text-gray-500 mb-2">Required Skills:</p>
        <div className="flex flex-wrap gap-2">
          {job.required_skills.slice(0, 5).map((skill, idx) => (
            <span key={idx} className="px-2 py-1 bg-purple-900 bg-opacity-50 rounded text-xs">
              {skill}
            </span>
          ))}
          {job.required_skills.length > 5 && (
            <span className="px-2 py-1 bg-gray-700 rounded text-xs">
              +{job.required_skills.length - 5}
            </span>
          )}
        </div>
      </div>

      <div className="flex gap-2">
        <Button
          onClick={() => onMatch(job.id)}
          disabled={loading}
          loading={loading}
          icon={TrendingUp}
          className="flex-1"
        >
          Match Candidates
        </Button>
        {onDelete && (
          <Button onClick={() => onDelete(job.id)} variant="secondary" className="px-3">
            Delete
          </Button>
        )}
      </div>
    </div>
  );
};

export default JobCard;
