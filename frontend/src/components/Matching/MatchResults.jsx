import React from 'react';
import { TrendingUp, Clock } from 'lucide-react';
import CandidateScore from './CandidateScore';
import LoadingSpinner from '../Common/LoadingSpinner';
import ErrorMessage from '../Common/ErrorMessage';

const MatchResults = ({ matches, loading, error, processingTime, jobTitle, onRetry }) => {
    if (loading) {
        return (
            <LoadingSpinner
                message="Analyzing candidates... This may take a minute per candidate."
                size="large"
            />
        );
    }

    if (error) {
        return (
            <ErrorMessage
                message={`Matching failed: ${error}`}
                onRetry={onRetry}
            />
        );
    }

    if (!matches || matches.length === 0) {
        return (
            <div className="text-center py-12">
                <TrendingUp className="w-16 h-16 mx-auto mb-4 text-gray-600" />
                <h3 className="text-xl font-semibold mb-2">No Matches Yet</h3>
                <p className="text-gray-400">
                    Upload resumes and select a job to see candidate matches
                </p>
            </div>
        );
    }

    return (
        <div>
            {/* Header */}
            <div className="mb-6">
                <h2 className="text-2xl font-semibold mb-2">
                    Top Matches {jobTitle && `for ${jobTitle}`}
                </h2>
                <div className="flex items-center gap-4 text-sm text-gray-400">
                    <span>{matches.length} candidates analyzed</span>
                    {processingTime > 0 && (
                        <span className="flex items-center gap-1">
                            <Clock className="w-4 h-4" />
                            Processed in {processingTime.toFixed(1)}s
                        </span>
                    )}
                </div>
            </div>

            {/* Match Cards */}
            <div className="space-y-6">
                {matches.map((match, index) => (
                    <CandidateScore
                        key={match.candidate_id}
                        match={match}
                        index={index}
                    />
                ))}
            </div>
        </div>
    );
};

export default MatchResults;