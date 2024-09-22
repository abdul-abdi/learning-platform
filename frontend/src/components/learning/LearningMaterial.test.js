import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import LearningMaterial from './LearningMaterial';
import { getLearningMaterial, updateUserProgress, updateUserAnalytics } from '../../services/api';

jest.mock('../../services/api');

describe('LearningMaterial Component', () => {
  const mockMaterial = {
    id: 1,
    title: 'Test Material',
    description: 'This is a test material',
    content: 'Test content'
  };

  beforeEach(() => {
    getLearningMaterial.mockResolvedValue({ data: mockMaterial });
    updateUserProgress.mockResolvedValue({});
    updateUserAnalytics.mockResolvedValue({});
  });

  test('renders learning material', async () => {
    render(<LearningMaterial materialId={1} />);

    await waitFor(() => {
      expect(screen.getByText(mockMaterial.title)).toBeInTheDocument();
      expect(screen.getByText(mockMaterial.description)).toBeInTheDocument();
    });
  });

  test('updates progress when slider is moved', async () => {
    render(<LearningMaterial materialId={1} />);

    await waitFor(() => {
      expect(screen.getByRole('slider')).toBeInTheDocument();
    });

    fireEvent.change(screen.getByRole('slider'), { target: { value: 50 } });
    fireEvent.click(screen.getByText(/update progress/i));

    await waitFor(() => {
      expect(updateUserProgress).toHaveBeenCalledWith({
        material_id: 1,
        progress_percentage: 50,
        status: 'in_progress'
      });
    });
  });

  test('shows quiz when "Take Quiz" button is clicked', async () => {
    render(<LearningMaterial materialId={1} />);

    await waitFor(() => {
      expect(screen.getByText(/take quiz/i)).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText(/take quiz/i));

    await waitFor(() => {
      expect(screen.getByText(/hide quiz/i)).toBeInTheDocument();
    });
  });
});