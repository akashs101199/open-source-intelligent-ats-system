import React, { useState } from 'react';
import Header from './components/Layout/Header';
import Navigation from './components/Layout/Navigation';
import JobList from './components/Jobs/JobList';
import JobForm from './components/Jobs/JobForm';
import CandidateUpload from './components/Candidates/CandidateUpload';
import CandidateList from './components/Candidates/CandidateList';
import MatchResults from './components/Matching/MatchResults';
import { useJobs } from './hooks/useJobs';
import { useCandidates } from './hooks/useCandidates';
import { useMatching } from './hooks/useMatching';

function App() {
    const [activeTab, setActiveTab] = useState('jobs');
    const [selectedJobId, setSelectedJobId] = useState(null);

    const { jobs, loading: jobsLoading, error: jobsError, createJob, deleteJob, fetchJobs } = useJobs();
    const { candidates, loading: candidatesLoading, error: candidatesError, uploadCandidate, fetchCandidates } = useCandidates();
    const { matches, loading: matchingLoading, error: matchingError, processingTime, matchCandidates } = useMatching();

    const handleCreateJob = async (jobData) => {
        await createJob(jobData);
        setActiveTab('jobs');
    };

    const handleUploadCandidate = async (file, candidateName) => {
        await uploadCandidate(file, candidateName);
    };

    const handleMatchCandidates = async (jobId) => {
        setSelectedJobId(jobId);
        await matchCandidates(jobId, 10, 0.0);
        setActiveTab('matches');
    };

    const selectedJob = jobs.find(job => job.id === selectedJobId);

    return (
        <div className="min-h-screen">
            <Header />

            <main className="container mx-auto px-4 py-8">
                <Navigation activeTab={activeTab} onTabChange={setActiveTab} />

                {/* Jobs Tab */}
                {activeTab === 'jobs' && (
                    <JobList
                        jobs={jobs}
                        loading={jobsLoading}
                        error={jobsError}
                        onMatch={handleMatchCandidates}
                        onDelete={deleteJob}
                        onRetry={fetchJobs}
                    />
                )}

                {/* Candidates Tab */}
                {activeTab === 'candidates' && (
                    <div className="space-y-8">
                        <CandidateUpload
                            onUpload={handleUploadCandidate}
                            loading={candidatesLoading}
                        />
                        <CandidateList
                            candidates={candidates}
                            loading={candidatesLoading}
                            error={candidatesError}
                            onRetry={fetchCandidates}
                        />
                    </div>
                )}

                {/* Matches Tab */}
                {activeTab === 'matches' && (
                    <MatchResults
                        matches={matches}
                        loading={matchingLoading}
                        error={matchingError}
                        processingTime={processingTime}
                        jobTitle={selectedJob?.title}
                        onRetry={() => selectedJobId && handleMatchCandidates(selectedJobId)}
                    />
                )}

                {/* Create Job Tab */}
                {activeTab === 'create' && (
                    <JobForm
                        onSubmit={handleCreateJob}
                        loading={jobsLoading}
                    />
                )}
            </main>

            {/* Footer */}
            <footer className="border-t border-gray-800 mt-16 py-6">
                <div className="container mx-auto px-4 text-center text-gray-400 text-sm">
                    <p>Intelligent ATS System v1.0 - Built for Agentic AI Roles</p>
                </div>
            </footer>
        </div>
    );
}

export default App;