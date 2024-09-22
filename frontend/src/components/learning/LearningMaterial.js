import React, { useState, useEffect, useRef } from 'react';
import { Paper, Typography, Button, Slider, Box } from '@material-ui/core';
import { getLearningMaterial, updateUserProgress, updateUserAnalytics } from '../../services/api';
import LearningMaterialProgress from './LearningMaterialProgress';
import Quiz from './Quiz';
import ForumPosts from '../forum/ForumPosts';

const LearningMaterial = ({ materialId }) => {
  const [material, setMaterial] = useState(null);
  const [progress, setProgress] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showQuiz, setShowQuiz] = useState(false);
  const [timeSpent, setTimeSpent] = useState(0);
  const [interactions, setInteractions] = useState(0);
  const intervalRef = useRef(null);

  useEffect(() => {
    const fetchMaterial = async () => {
      try {
        const response = await getLearningMaterial(materialId);
        setMaterial(response.data);
        setProgress(response.data.user_progress?.progress_percentage || 0);
        setLoading(false);
      } catch (err) {
        setError('Failed to load learning material');
        setLoading(false);
      }
    };

    fetchMaterial();

    // Start tracking time spent
    intervalRef.current = setInterval(() => {
      setTimeSpent((prevTime) => prevTime + 1);
    }, 1000);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [materialId]);

  const handleProgressChange = (event, newValue) => {
    setProgress(newValue);
  };

  const handleInteraction = () => {
    setInteractions((prevInteractions) => prevInteractions + 1);
  };

  const handleProgressUpdate = async () => {
    try {
      await updateUserProgress({
        material_id: materialId,
        progress_percentage: progress,
        status: progress === 100 ? 'completed' : 'in_progress'
      });

      await updateUserAnalytics({
        material_id: materialId,
        time_spent: timeSpent,
        interactions: interactions
      });

      // Reset analytics tracking
      setTimeSpent(0);
      setInteractions(0);

      // Optionally, you can show a success message here
    } catch (err) {
      setError('Failed to update progress and analytics');
    }
  };

  if (loading) return <Typography>Loading...</Typography>;
  if (error) return <Typography color="error">{error}</Typography>;
  if (!material) return <Typography>No material found</Typography>;

  return (
    <Paper style={{ padding: '2rem', marginTop: '2rem' }} onClick={handleInteraction}>
      <Typography variant="h4" gutterBottom>{material.title}</Typography>
      <Typography variant="body1" paragraph>{material.description}</Typography>
      <Box my={4}>
        <Typography gutterBottom>Your Progress</Typography>
        <LearningMaterialProgress progress={progress} />
      </Box>
      <Box my={4}>
        <Typography gutterBottom>Update Progress</Typography>
        <Slider
          value={progress}
          onChange={handleProgressChange}
          aria-labelledby="continuous-slider"
          valueLabelDisplay="auto"
          step={1}
          marks
          min={0}
          max={100}
        />
      </Box>
      <Button variant="contained" color="primary" onClick={handleProgressUpdate}>
        Update Progress
      </Button>
      <Button variant="contained" color="secondary" onClick={() => setShowQuiz(!showQuiz)} style={{ marginLeft: '1rem' }}>
        {showQuiz ? 'Hide Quiz' : 'Take Quiz'}
      </Button>
      {showQuiz && <Quiz materialId={materialId} />}
      <ForumPosts materialId={materialId} />
    </Paper>
  );
};

export default LearningMaterial;