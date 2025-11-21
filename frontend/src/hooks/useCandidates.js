import { useState, useEffect } from 'react';
import { candidatesApi } from '../services/api';

export const useCandidates = () => {
    const [candidates, setCandidates] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchCandidates = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await candidatesApi.list();
            setCandidates(response.data.candidates || []);
        } catch (err) {
            setError(err.response?.data?.detail || err.message);
            console.error('Error fetching candidates:', err);
        } finally {
            setLoading(false);
        }
    };

    const uploadCandidate = async (file, candidateName) => {
        setLoading(true);
        setError(null);
        try {
            const response = await candidatesApi.upload(file, candidateName);
            await fetchCandidates(); // Refresh list
            return response.data;
        } catch (err) {
            setError(err.response?.data?.detail || err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    };

    const deleteCandidate = async (candidateId) => {
        setLoading(true);
        setError(null);
        try {
            await candidatesApi.delete(candidateId);
            await fetchCandidates(); // Refresh list
        } catch (err) {
            setError(err.response?.data?.detail || err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchCandidates();
    }, []);

    return { candidates, loading, error, fetchCandidates, uploadCandidate, deleteCandidate };
};