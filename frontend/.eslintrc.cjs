module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'prettier',
  ],
  parser: '@babel/eslint-parser',
  parserOptions: {
    requireConfigFile: false,
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 12,
    sourceType: 'module',
    babelOptions: {
      presets: ['@babel/preset-react'],
    },
  },
  plugins: ['react', 'react-hooks', 'prettier'],
  rules: {
    'react/react-in-jsx-scope': 'off',
    'no-unused-vars': 'warn',
    'prettier/prettier': 'error',
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
};
