import React from 'react';

const Input = ({
    label,
    error,
    helperText,
    className = '',
    ...props
}) => {
    return (
        <div className={`mb-4 ${className}`}>
            {label && (
                <label className="block text-sm font-medium mb-2">
                    {label}
                    {props.required && <span className="text-red-400 ml-1">*</span>}
                </label>
            )}
            <input
                className="input-field"
                {...props}
            />
            {error && (
                <p className="text-red-400 text-sm mt-1">{error}</p>
            )}
            {helperText && !error && (
                <p className="text-gray-400 text-sm mt-1">{helperText}</p>
            )}
        </div>
    );
};

export default Input;