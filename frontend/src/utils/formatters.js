export const formatPercentage = value => {
  return `${(value * 100).toFixed(1)}%`;
};

export const formatDate = dateString => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

export const formatFileSize = bytes => {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
};

export const getScoreLabel = score => {
  if (score >= 0.8) return 'Excellent Match';
  if (score >= 0.6) return 'Good Match';
  if (score >= 0.4) return 'Moderate Match';
  return 'Weak Match';
};

export const getScoreColor = score => {
  if (score >= 0.8) return 'text-green-400 bg-green-900';
  if (score >= 0.6) return 'text-blue-400 bg-blue-900';
  if (score >= 0.4) return 'text-yellow-400 bg-yellow-900';
  return 'text-red-400 bg-red-900';
};

export const truncateText = (text, maxLength = 100) => {
  if (!text || text.length <= maxLength) return text;
  return `${text.substring(0, maxLength)}...`;
};
