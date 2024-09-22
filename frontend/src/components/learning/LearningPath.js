import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Typography, Paper, List, ListItem, ListItemText, Button, LinearProgress } from '@material-ui/core';
import { getLearningPath, getUserLearningPathProgress } from '../../services/api';

const LearningPath = () => {
  const { pathId } = useParams();
  const [learningPath, setLearningPath] = useState(null);
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLearningPathData = async () => {
      try {
        const [pathResponse, progressResponse] = await Promise.all([
          getLearningPath(pathId),
          getUserLearningPathProgress(pathId)
        ]);
        setLearningPath(pathResponse.data);
        setProgress(progressResponse.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to load learning path data');
        setLoading(false);
      }
    };

    fetchLearningPathData();
  }, [pathId]);

  if (loading) return <Typography>Loading learning path...</Typography>;
  if (error) return <Typography color="error">{error}</Typography>;

  return (
    <Paper style={{ padding: '1rem' }}>
      <Typography variant="h4" gutterBottom>{learningPath.title}</Typography>
      <Typography variant="body1" paragraph>{learningPath.description}</Typography>
      <Typography variant="h6" gutterBottom>Overall Progress</Typography>
      <LinearProgress 
        variant="determinate" 
        value={progress.overall_progress} 
        style={{ marginBottom: '1rem' }}
      />
      <Typography variant="h6" gutterBottom>Materials</Typography>
      <List>
        {learningPath.materials.map((material, index) => (
          <ListItem key={material.id}>
            <ListItemText 
              primary={`${index + 1}. ${material.material.title}`}
              secondary={`Progress: ${progress.materials_progress[index].progress_percentage}%`}
            />
            <Button 
              variant="contained" 
              color="primary" 
              component={Link} 
              to={`/learning-material/${material.material_id}`}
            >
              Start
            </Button>
          </ListItem>
        ))}
      </List>
    </Paper>
  );
};

export default LearningPath;