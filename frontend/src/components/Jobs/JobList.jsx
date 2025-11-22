import React from 'react';
import { Briefcase } from 'lucide-react';
import JobCard from './JobCard';
import LoadingSpinner from '../Common/LoadingSpinner';
import ErrorMessage from '../Common/ErrorMessage';

const JobList = ({ jobs, loading, error, onMatch, onDelete, onRetry }) => {
  if (loading && jobs.length === 0) {
    return <LoadingSpinner message="Loading jobs..." />;
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={onRetry} />;
  }

  if (jobs.length === 0) {
    return (
      <div className="text-center py-12">
        <Briefcase className="w-16 h-16 mx-auto mb-4 text-gray-600" />
        <h3 className="text-xl font-semibold mb-2">No Jobs Yet</h3>
        <p className="text-gray-400 mb-6">Create your first job to get started!</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {jobs.map(job => (
        <JobCard key={job.id} job={job} onMatch={onMatch} onDelete={onDelete} loading={loading} />
      ))}
    </div>
  );
};

export default JobList;
