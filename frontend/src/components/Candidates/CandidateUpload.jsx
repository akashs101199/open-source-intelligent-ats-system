import React, { useState, useRef } from 'react';
import { Upload, FileText, CheckCircle } from 'lucide-react';
import Button from '../Common/Button';
import { FILE_TYPES } from '../../utils/constants';
import { formatFileSize } from '../../utils/formatters';

const CandidateUpload = ({ onUpload, loading }) => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [candidateName, setCandidateName] = useState('');
    const [dragActive, setDragActive] = useState(false);
    const fileInputRef = useRef(null);

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true);
        } else if (e.type === 'dragleave') {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0]);
        }
    };

    const handleChange = (e) => {
        e.preventDefault();
        if (e.target.files && e.target.files[0]) {
            handleFile(e.target.files[0]);
        }
    };

    const handleFile = (file) => {
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();

        if (!FILE_TYPES.ALLOWED.includes(fileExtension)) {
            alert(`Invalid file type. Allowed types: ${FILE_TYPES.ALLOWED.join(', ')}`);
            return;
        }

        if (file.size > FILE_TYPES.MAX_SIZE_MB * 1024 * 1024) {
            alert(`File size exceeds ${FILE_TYPES.MAX_SIZE_MB}MB limit`);
            return;
        }

        setSelectedFile(file);
        if (!candidateName) {
            setCandidateName(file.name.replace(/\.[^/.]+$/, ''));
        }
    };

    const handleUpload = async () => {
        if (!selectedFile) return;

        try {
            await onUpload(selectedFile, candidateName);
            setSelectedFile(null);
            setCandidateName('');
        } catch (err) {
            console.error('Upload error:', err);
        }
    };

    return (
        <div className="card p-8">
            <h2 className="text-2xl font-semibold mb-6">Upload Resume</h2>

            {!selectedFile ? (
                <div
                    className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${dragActive
                        ? 'border-purple-500 bg-purple-500 bg-opacity-10'
                        : 'border-gray-600 hover:border-gray-500'
                        }`}
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                >
                    <Upload className="w-16 h-16 mx-auto mb-4 text-gray-500" />
                    <input
                        ref={fileInputRef}
                        type="file"
                        onChange={handleChange}
                        accept={FILE_TYPES.ALLOWED.join(',')}
                        className="hidden"
                        disabled={loading}
                    />
                    <Button
                        onClick={() => fileInputRef.current?.click()}
                        disabled={loading}
                        className="mb-3"
                    >
                        Choose Resume
                    </Button>
                    <p className="text-sm text-gray-400 mb-1">
                        or drag and drop your file here
                    </p>
                    <p className="text-xs text-gray-500">
                        Supported formats: {FILE_TYPES.ALLOWED.join(', ')} (Max {FILE_TYPES.MAX_SIZE_MB}MB)
                    </p>
                </div>
            ) : (
                <div className="space-y-4">
                    <div className="flex items-center gap-4 p-4 bg-gray-900 rounded-lg">
                        <FileText className="w-10 h-10 text-purple-400" />
                        <div className="flex-1">
                            <p className="font-medium">{selectedFile.name}</p>
                            <p className="text-sm text-gray-400">{formatFileSize(selectedFile.size)}</p>
                        </div>
                        <CheckCircle className="w-6 h-6 text-green-400" />
                    </div>

                    <div>
                        <label className="block text-sm font-medium mb-2">
                            Candidate Name (optional)
                        </label>
                        <input
                            className="input-field"
                            value={candidateName}
                            onChange={(e) => setCandidateName(e.target.value)}
                            placeholder="Enter candidate name or leave blank"
                        />
                    </div>

                    <div className="flex gap-3">
                        <Button
                            onClick={handleUpload}
                            disabled={loading}
                            loading={loading}
                            className="flex-1"
                        >
                            {loading ? 'Uploading...' : 'Upload & Index'}
                        </Button>
                        <Button
                            onClick={() => {
                                setSelectedFile(null);
                                setCandidateName('');
                            }}
                            variant="secondary"
                            disabled={loading}
                        >
                            Cancel
                        </Button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default CandidateUpload;