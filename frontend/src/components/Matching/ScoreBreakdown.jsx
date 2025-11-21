import React from 'react';

const ScoreBreakdown = ({ scores, labels }) => {
    const scoreData = [
        { key: 'agentic_capabilities', label: labels?.agentic || 'Agentic Capabilities', value: scores.agentic_capabilities },
        { key: 'technical_depth', label: labels?.technical || 'Technical Depth', value: scores.technical_depth },
        { key: 'semantic_match', label: labels?.semantic || 'Semantic Match', value: scores.semantic_match },
        { key: 'experience_quality', label: labels?.experience || 'Experience Quality', value: scores.experience_quality },
    ];

    return (
        <div className="space-y-3">
            {scoreData.map((item) => (
                <div key={item.key}>
                    <div className="flex justify-between text-sm mb-1">
                        <span className="text-gray-300">{item.label}</span>
                        <span className="font-semibold">{(item.value * 100).toFixed(1)}%</span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-2.5">
                        <div
                            className="h-2.5 rounded-full transition-all duration-500"
                            style={{
                                width: `${item.value * 100}%`,
                                backgroundColor:
                                    item.value > 0.7
                                        ? '#10b981'
                                        : item.value > 0.5
                                            ? '#3b82f6'
                                            : item.value > 0.3
                                                ? '#f59e0b'
                                                : '#ef4444',
                            }}
                        />
                    </div>
                </div>
            ))}
        </div>
    );
};

export default ScoreBreakdown;