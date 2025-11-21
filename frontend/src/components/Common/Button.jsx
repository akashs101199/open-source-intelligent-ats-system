import React from 'react';
import { Loader2 } from 'lucide-react';

const Button = ({
    children,
    onClick,
    disabled,
    loading,
    variant = 'primary',
    type = 'button',
    className = '',
    icon: Icon,
    ...props
}) => {
    const baseClasses = 'px-4 py-2 rounded font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2';

    const variants = {
        primary: 'bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700',
        secondary: 'bg-gray-700 hover:bg-gray-600',
        danger: 'bg-red-600 hover:bg-red-700',
        outline: 'border-2 border-purple-500 hover:bg-purple-500 hover:bg-opacity-10',
    };

    return (
        <button
            type={type}
            onClick={onClick}
            disabled={disabled || loading}
            className={`${baseClasses} ${variants[variant]} ${className}`}
            {...props}
        >
            {loading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
            ) : Icon ? (
                <Icon className="w-4 h-4" />
            ) : null}
            {children}
        </button>
    );
};

export default Button;