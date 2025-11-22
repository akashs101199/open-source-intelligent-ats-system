import { useState } from 'react';
import { matchingApi } from '../services/api';

export const useMatching = () => {
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [processingTime, setProcessingTime] = useState(0);

  const matchCandidates = async (jobId, topK = 10, minScore = 0.0) => {
    setLoading(true);
    setError(null);
    setMatches([]);
    try {
      const response = await matchingApi.matchCandidates(jobId, topK, minScore);
      setMatches(response.data.matches || []);
      setProcessingTime(response.data.processing_time_seconds || 0);
      return response.data;
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const getScore = async (jobId, candidateId) => {
    setLoading(true);
    setError(null);
    try {
      const response = await matchingApi.getScore(jobId, candidateId);
      return response.data;
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { matches, loading, error, processingTime, matchCandidates, getScore };
};
