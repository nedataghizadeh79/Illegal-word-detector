import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

// this is the main root. We call just App component to show all it's children
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

