import React, { useState, useEffect } from 'react';
import { getUserProgress, getRecommendations } from '../services/api';
import ProgressTracker from './ProgressTracker';
import RecommendationList from './RecommendationList';
import Feedback from './Feedback';
import { useTheme } from '../contexts/ThemeContext';

const Dashboard = () => {
  const [progress, setProgress] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { darkMode } = useTheme();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [progressData, recommendationsData] = await Promise.all([
          getUserProgress(),
          getRecommendations()
        ]);
        setProgress(progressData);
        setRecommendations(recommendationsData);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        setError('Failed to load dashboard data. Please try again.');
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return <div className="text-center mt-8">Loading...</div>;
  }

  if (error) {
    return <div className="text-center mt-8 text-red-500">{error}</div>;
  }

  return (
    <div className={`p-6 ${darkMode ? 'bg-gray-900 text-white' : 'bg-gray-100 text-gray-900'}`}>
      <h1 className="text-3xl font-bold mb-6">Your Learning Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h2 className="text-xl font-semibold mb-4">Your Progress</h2>
          {progress && <ProgressTracker progress={progress} />}
        </div>
        <div>
          <h2 className="text-xl font-semibold mb-4">Recommended Materials</h2>
          <RecommendationList recommendations={recommendations} />
        </div>
      </div>
      <Feedback />
    </div>
  );
};

export default Dashboard;