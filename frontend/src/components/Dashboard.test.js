import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import Dashboard from './Dashboard';
import { getUserProgress, getRecommendations } from '../services/api';
import { AuthProvider } from '../contexts/AuthContext';

jest.mock('../services/api');

describe('Dashboard Component', () => {
  beforeEach(() => {
    getUserProgress.mockResolvedValue({
      data: [
        { id: 1, title: 'Material 1', progress: 50 },
        { id: 2, title: 'Material 2', progress: 75 },
      ],
    });
    getRecommendations.mockResolvedValue({
      data: [
        { id: 3, title: 'Recommended Material 1' },
        { id: 4, title: 'Recommended Material 2' },
      ],
    });
  });

  test('renders user progress and recommendations', async () => {
    render(
      <AuthProvider>
        <Dashboard />
      </AuthProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('Your Learning Dashboard')).toBeInTheDocument();
      expect(screen.getByText('Your Progress')).toBeInTheDocument();
      expect(screen.getByText('Recommended Materials')).toBeInTheDocument();
      expect(screen.getByText('Material 1')).toBeInTheDocument();
      expect(screen.getByText('Material 2')).toBeInTheDocument();
      expect(screen.getByText('Recommended Material 1')).toBeInTheDocument();
      expect(screen.getByText('Recommended Material 2')).toBeInTheDocument();
    });
  });

  test('displays loading state', () => {
    getUserProgress.mockReturnValue(new Promise(() => {}));
    getRecommendations.mockReturnValue(new Promise(() => {}));

    render(
      <AuthProvider>
        <Dashboard />
      </AuthProvider>
    );

    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  test('handles error state', async () => {
    getUserProgress.mockRejectedValue(new Error('Failed to fetch progress'));
    getRecommendations.mockRejectedValue(new Error('Failed to fetch recommendations'));

    render(
      <AuthProvider>
        <Dashboard />
      </AuthProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('Error loading dashboard data')).toBeInTheDocument();
    });
  });
});