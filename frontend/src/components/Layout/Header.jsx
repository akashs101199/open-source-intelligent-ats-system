import React from 'react';
import { Bot, Github } from 'lucide-react';

const Header = () => {
    return (
        <header className="border-b border-gray-800">
            <div className="container mx-auto px-4 py-6">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="bg-gradient-to-br from-purple-500 to-pink-500 p-3 rounded-lg">
                            <Bot className="w-8 h-8" />
                        </div>
                        <div>
                            <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                                Intelligent ATS
                            </h1>
                            <p className="text-sm text-gray-400">Multi-Agent System for Agentic AI Roles</p>
                        </div>
                    </div>

                    href="https://github.com/yourusername/intelligent-ats"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors"
          >
                    <Github className="w-5 h-5" />
                    <span className="hidden sm:inline">GitHub</span>
                </a>
            </div>
        </div>
    </header >
  );
};

export default Header;