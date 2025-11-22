import { useState, useEffect } from 'react';
import { jobsApi } from '../services/api';

export const useJobs = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchJobs = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await jobsApi.list();
      setJobs(response.data.jobs || []);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
      console.error('Error fetching jobs:', err);
    } finally {
      setLoading(false);
    }
  };

  const createJob = async jobData => {
    setLoading(true);
    setError(null);
    try {
      const response = await jobsApi.create(jobData);
      await fetchJobs(); // Refresh list
      return response.data;
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const deleteJob = async jobId => {
    setLoading(true);
    setError(null);
    try {
      await jobsApi.delete(jobId);
      await fetchJobs(); // Refresh list
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, []);

  return { jobs, loading, error, fetchJobs, createJob, deleteJob };
};
