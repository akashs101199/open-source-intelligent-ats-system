import React from 'react';
import { Briefcase, Users, TrendingUp, FileText } from 'lucide-react';

const Navigation = ({ activeTab, onTabChange }) => {
  const tabs = [
    { id: 'jobs', label: 'Jobs', icon: Briefcase },
    { id: 'candidates', label: 'Candidates', icon: Users },
    { id: 'matches', label: 'Matches', icon: TrendingUp },
    { id: 'create', label: 'Create Job', icon: FileText },
  ];

  return (
    <nav className="border-b border-gray-700 mb-6">
      <div className="flex space-x-1 overflow-x-auto">
        {tabs.map(tab => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={`px-4 py-3 font-medium transition-colors whitespace-nowrap flex items-center gap-2 ${
                activeTab === tab.id
                  ? 'border-b-2 border-purple-500 text-purple-400'
                  : 'text-gray-400 hover:text-gray-200'
              }`}
            >
              <Icon className="w-4 h-4" />
              {tab.label}
            </button>
          );
        })}
      </div>
    </nav>
  );
};

export default Navigation;
