import React from 'react';
import { Users } from 'lucide-react';
import CandidateCard from './CandidateCard';
import LoadingSpinner from '../Common/LoadingSpinner';
import ErrorMessage from '../Common/ErrorMessage';

const CandidateList = ({ candidates, loading, error, onDelete, onRetry }) => {
    if (loading && candidates.length === 0) {
        return <LoadingSpinner message="Loading candidates..." />;
    }

    if (error) {
        return <ErrorMessage message={error} onRetry={onRetry} />;
    }

    if (candidates.length === 0) {
        return (
            <div className="text-center py-12">
                <Users className="w-16 h-16 mx-auto mb-4 text-gray-600" />
                <h3 className="text-xl font-semibold mb-2">No Candidates Yet</h3>
                <p className="text-gray-400 mb-6">Upload resumes to build your candidate pool</p>
            </div>
        );
    }

    return (
        <div>
            <div className="mb-6">
                <h2 className="text-2xl font-semibold">Candidate Pool</h2>
                <p className="text-gray-400 mt-1">{candidates.length} candidates indexed</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {candidates.map((candidate) => (
                    <CandidateCard
                        key={candidate.id}
                        candidate={candidate}
                        onDelete={onDelete}
                    />
                ))}
            </div>
        </div>
    );
};

export default CandidateList;