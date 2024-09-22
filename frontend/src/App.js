import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { ThemeProvider } from './contexts/ThemeContext';
import Layout from './components/Layout';

function App() {
  return (
    <AuthProvider>
      <ThemeProvider>
        <Router>
          <Layout />
        </Router>
      </ThemeProvider>
    </AuthProvider>
  );
}

export default App;