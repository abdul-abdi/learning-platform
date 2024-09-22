import React, { useState, useEffect } from 'react';
import { List, ListItem, ListItemText, Typography, Paper, Button } from '@material-ui/core';
import { Link } from 'react-router-dom';
import { getLearningPaths } from '../../services/api';

const LearningPathList = () => {
  const [learningPaths, setLearningPaths] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLearningPaths = async () => {
      try {
        const response = await getLearningPaths();
        setLearningPaths(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to load learning paths');
        setLoading(false);
      }
    };

    fetchLearningPaths();
  }, []);

  if (loading) return <Typography>Loading learning paths...</Typography>;
  if (error) return <Typography color="error">{error}</Typography>;

  return (
    <Paper style={{ padding: '1rem' }}>
      <Typography variant="h5" gutterBottom>Learning Paths</Typography>
      <List>
        {learningPaths.map((path) => (
          <ListItem key={path.id}>
            <ListItemText 
              primary={path.title}
              secondary={path.description}
            />
            <Button 
              component={Link} 
              to={`/learning-path/${path.id}`}
              variant="contained" 
              color="primary"
            >
              View Path
            </Button>
          </ListItem>
        ))}
      </List>
    </Paper>
  );
};

export default LearningPathList;