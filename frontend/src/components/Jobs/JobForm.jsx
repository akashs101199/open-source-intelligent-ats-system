import React, { useState } from 'react';
import { Plus, X } from 'lucide-react';
import Button from '../Common/Button';
import Input from '../Common/Input';
import { EXPERIENCE_LEVELS } from '../../utils/constants';

const JobForm = ({ onSubmit, loading }) => {
    const [formData, setFormData] = useState({
        title: '',
        description: '',
        responsibilities: [''],
        required_skills: '',
        preferred_skills: '',
        experience_level: 'mid',
        company: '',
    });

    const [errors, setErrors] = useState({});

    const validateForm = () => {
        const newErrors = {};

        if (!formData.title.trim()) {
            newErrors.title = 'Job title is required';
        }
        if (!formData.description.trim()) {
            newErrors.description = 'Description is required';
        }
        if (formData.responsibilities.filter(r => r.trim()).length === 0) {
            newErrors.responsibilities = 'At least one responsibility is required';
        }
        if (!formData.required_skills.trim()) {
            newErrors.required_skills = 'Required skills are required';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = async () => {
        if (!validateForm()) return;

        const jobData = {
            ...formData,
            responsibilities: formData.responsibilities.filter(r => r.trim()),
            required_skills: formData.required_skills.split(',').map(s => s.trim()).filter(s => s),
            preferred_skills: formData.preferred_skills.split(',').map(s => s.trim()).filter(s => s),
        };

        try {
            await onSubmit(jobData);
            // Reset form on success
            setFormData({
                title: '',
                description: '',
                responsibilities: [''],
                required_skills: '',
                preferred_skills: '',
                experience_level: 'mid',
                company: '',
            });
        } catch (err) {
            console.error('Error creating job:', err);
        }
    };

    const addResponsibility = () => {
        setFormData({
            ...formData,
            responsibilities: [...formData.responsibilities, ''],
        });
    };

    const updateResponsibility = (index, value) => {
        const newResponsibilities = [...formData.responsibilities];
        newResponsibilities[index] = value;
        setFormData({ ...formData, responsibilities: newResponsibilities });
    };

    const removeResponsibility = (index) => {
        const newResponsibilities = formData.responsibilities.filter((_, i) => i !== index);
        setFormData({ ...formData, responsibilities: newResponsibilities });
    };

    return (
        <div className="max-w-2xl mx-auto">
            <div className="card p-8">
                <h2 className="text-2xl font-semibold mb-6">Create Job Description</h2>

                <Input
                    label="Job Title"
                    value={formData.title}
                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                    placeholder="e.g., Senior Agentic AI Engineer"
                    error={errors.title}
                    required
                />

                <div className="mb-4">
                    <label className="block text-sm font-medium mb-2">
                        Company <span className="text-gray-500">(optional)</span>
                    </label>
                    <input
                        className="input-field"
                        value={formData.company}
                        onChange={(e) => setFormData({ ...formData, company: e.target.value })}
                        placeholder="Your company name"
                    />
                </div>

                <div className="mb-4">
                    <label className="block text-sm font-medium mb-2">
                        Description <span className="text-red-400">*</span>
                    </label>
                    <textarea
                        className="input-field h-24"
                        value={formData.description}
                        onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                        placeholder="Brief overview of the role and what makes it exciting..."
                        required
                    />
                    {errors.description && (
                        <p className="text-red-400 text-sm mt-1">{errors.description}</p>
                    )}
                </div>

                <div className="mb-4">
                    <label className="block text-sm font-medium mb-2">
                        Key Responsibilities <span className="text-red-400">*</span>
                    </label>
                    {formData.responsibilities.map((resp, index) => (
                        <div key={index} className="flex gap-2 mb-2">
                            <input
                                className="input-field"
                                value={resp}
                                onChange={(e) => updateResponsibility(index, e.target.value)}
                                placeholder="e.g., Design and implement multi-agent systems"
                            />
                            {formData.responsibilities.length > 1 && (
                                <Button
                                    onClick={() => removeResponsibility(index)}
                                    variant="secondary"
                                    className="px-3"
                                >
                                    <X className="w-4 h-4" />
                                </Button>
                            )}
                        </div>
                    ))}
                    <Button
                        onClick={addResponsibility}
                        variant="outline"
                        className="w-full mt-2"
                        icon={Plus}
                    >
                        Add Responsibility
                    </Button>
                    {errors.responsibilities && (
                        <p className="text-red-400 text-sm mt-1">{errors.responsibilities}</p>
                    )}
                </div>

                <Input
                    label="Required Skills (comma-separated)"
                    value={formData.required_skills}
                    onChange={(e) => setFormData({ ...formData, required_skills: e.target.value })}
                    placeholder="LangChain, LLMs, Python, Multi-agent systems"
                    error={errors.required_skills}
                    helperText="Separate skills with commas"
                    required
                />

                <Input
                    label="Preferred Skills (comma-separated)"
                    value={formData.preferred_skills}
                    onChange={(e) => setFormData({ ...formData, preferred_skills: e.target.value })}
                    placeholder="CrewAI, AutoGPT, Vector databases"
                    helperText="Optional: Nice-to-have skills"
                />

                <div className="mb-6">
                    <label className="block text-sm font-medium mb-2">
                        Experience Level <span className="text-red-400">*</span>
                    </label>
                    <select
                        className="input-field"
                        value={formData.experience_level}
                        onChange={(e) => setFormData({ ...formData, experience_level: e.target.value })}
                    >
                        {Object.entries(EXPERIENCE_LEVELS).map(([value, label]) => (
                            <option key={value} value={value}>
                                {label}
                            </option>
                        ))}
                    </select>
                </div>

                <Button
                    onClick={handleSubmit}
                    disabled={loading}
                    loading={loading}
                    className="w-full"
                >
                    {loading ? 'Creating...' : 'Create Job'}
                </Button>
            </div>
        </div>
    );
};

export default JobForm;