import React from 'react';
import { useTheme } from '../contexts/ThemeContext';
import Navbar from './Navbar';

const Layout = ({ children }) => {
  const { darkMode } = useTheme();

  return (
    <div className={`min-h-screen ${darkMode ? 'dark' : ''}`}>
      <div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
        <a href="#main-content" className="sr-only focus:not-sr-only">
          Skip to main content
        </a>
        <Navbar />
        <main id="main-content" className="container mx-auto px-4 py-8">
          {children}
        </main>
        <footer className="bg-gray-100 dark:bg-gray-800 p-4 mt-8">
          <div className="container mx-auto text-center">
            <p>&copy; 2023 AI-Driven Personalized Learning Platform. All rights reserved.</p>
          </div>
        </footer>
      </div>
    </div>
  );
};

export default Layout;