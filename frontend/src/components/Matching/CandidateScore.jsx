import React, { useState } from 'react';
import { ChevronDown, ChevronUp, CheckCircle, AlertCircle, User } from 'lucide-react';
import ScoreBreakdown from './ScoreBreakdown';
import { getScoreLabel, getScoreColor } from '../../utils/formatters';

const CandidateScore = ({ match, index }) => {
  const [expanded, setExpanded] = useState(false);

  const overallPercentage = (match.overall_score * 100).toFixed(1);

  return (
    <div className="card p-6 hover:border-purple-500 transition-colors">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-start gap-3">
          <div className="bg-purple-900 bg-opacity-50 p-3 rounded-lg">
            <User className="w-6 h-6 text-purple-400" />
          </div>
          <div>
            <h3 className="text-xl font-semibold">Candidate #{match.candidate_id.split('_')[1]}</h3>
            <p className="text-sm text-gray-400">
              Overall Score: <span className="font-semibold text-white">{overallPercentage}%</span>
            </p>
          </div>
        </div>
        <div
          className={`px-4 py-2 rounded-lg font-semibold text-sm ${getScoreColor(match.overall_score)}`}
        >
          {getScoreLabel(match.overall_score)}
        </div>
      </div>

      {/* Score Breakdown */}
      <div className="mb-4">
        <ScoreBreakdown scores={match} />
      </div>

      {/* AI Analysis */}
      {match.reasoning && (
        <div className="bg-gray-900 bg-opacity-50 rounded-lg p-4 mb-4">
          <h4 className="font-semibold text-sm mb-2 text-purple-300 flex items-center gap-2">
            <AlertCircle className="w-4 h-4" />
            AI Analysis
          </h4>
          <p className="text-sm text-gray-300 leading-relaxed">{match.reasoning}</p>
        </div>
      )}

      {/* Expand/Collapse Button */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between text-purple-400 hover:text-purple-300 transition-colors py-2"
      >
        <span className="text-sm font-medium">
          {expanded ? 'Hide Details' : 'Show Detailed Analysis'}
        </span>
        {expanded ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
      </button>

      {/* Expanded Details */}
      {expanded && (
        <div className="pt-4 mt-4 border-t border-gray-700 space-y-4">
          {/* Strengths */}
          {match.strengths && match.strengths.length > 0 && (
            <div>
              <h4 className="font-semibold text-sm mb-3 text-green-400 flex items-center gap-2">
                <CheckCircle className="w-4 h-4" />
                Key Strengths
              </h4>
              <ul className="space-y-2">
                {match.strengths.map((strength, idx) => (
                  <li key={idx} className="flex items-start gap-2 text-sm text-gray-300">
                    <span className="text-green-400 mt-0.5">✓</span>
                    <span>{strength}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Gaps */}
          {match.gaps && match.gaps.length > 0 && (
            <div>
              <h4 className="font-semibold text-sm mb-3 text-orange-400 flex items-center gap-2">
                <AlertCircle className="w-4 h-4" />
                Areas for Consideration
              </h4>
              <ul className="space-y-2">
                {match.gaps.map((gap, idx) => (
                  <li key={idx} className="flex items-start gap-2 text-sm text-gray-300">
                    <span className="text-orange-400 mt-0.5">!</span>
                    <span>{gap}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default CandidateScore;
