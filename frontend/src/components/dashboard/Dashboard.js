import React, { useState, useEffect } from 'react';
import { Container, Typography, Grid, Paper, List, ListItem, ListItemText, Button, CircularProgress, Pagination } from '@material-ui/core';
import { Alert } from '@material-ui/lab';
import { getUserProgress, getRecommendations, getLearningMaterial, getLearningMaterials, getUserBadges, getNotifications } from '../../services/api';
import LearningMaterialProgress from '../learning/LearningMaterialProgress';
import LearningMaterialSearch from '../learning/LearningMaterialSearch';
import UserStatistics from './UserStatistics';
import UserBadges from './UserBadges';
import Notifications from '../notifications/Notifications';

const Dashboard = () => {
  const [userProgress, setUserProgress] = useState({ items: [], total: 0, pages: 1 });
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [searchResults, setSearchResults] = useState([]);
  const [userBadges, setUserBadges] = useState([]);
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [progressResponse, recommendationsResponse, badgesResponse, notificationsResponse] = await Promise.all([
          getUserProgress(page),
          getRecommendations(),
          getUserBadges(),
          getNotifications()
        ]);
        setUserProgress(progressResponse.data);
        setRecommendations(recommendationsResponse.data);
        setUserBadges(badgesResponse.data);
        setNotifications(notificationsResponse.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        setError('Failed to load dashboard data. Please try again later.');
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, [page]);

  const handlePageChange = (event, value) => {
    setPage(value);
  };

  const handleStartLearning = async (materialId) => {
    try {
      const material = await getLearningMaterial(materialId);
      // Navigate to the learning material page
      // This is a placeholder - you'll need to implement the actual navigation
      console.log('Starting learning material:', material.data);
    } catch (error) {
      console.error('Error fetching learning material:', error);
      setError('Failed to start learning material. Please try again.');
    }
  };

  const handleSearch = async (query) => {
    try {
      const response = await getLearningMaterials(1, 10, query);
      setSearchResults(response.data.items);
    } catch (error) {
      console.error('Error searching learning materials:', error);
      setError('Failed to search learning materials. Please try again.');
    }
  };

  if (loading) {
    return (
      <Container maxWidth="lg" style={{ marginTop: '2rem', textAlign: 'center' }}>
        <CircularProgress />
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg" style={{ marginTop: '2rem' }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" style={{ marginTop: '2rem' }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Your Learning Dashboard
      </Typography>
      <Grid container spacing={4}>
        <Grid item xs={12} md={8}>
          <UserStatistics userProgress={userProgress} />
          <Paper style={{ padding: '1rem', marginTop: '1rem' }}>
            <Typography variant="h6" gutterBottom>Your Progress</Typography>
            {userProgress.items.length > 0 ? (
              <>
                <List>
                  {userProgress.items.map((progress) => (
                    <ListItem key={progress.id}>
                      <ListItemText 
                        primary={progress.learning_material.title}
                        secondary={
                          <LearningMaterialProgress progress={progress.progress_percentage} />
                        }
                      />
                    </ListItem>
                  ))}
                </List>
                <Pagination 
                  count={userProgress.pages} 
                  page={page} 
                  onChange={handlePageChange} 
                  color="primary" 
                  style={{ marginTop: '1rem', display: 'flex', justifyContent: 'center' }}
                />
              </>
            ) : (
              <Typography>No progress recorded yet. Start learning!</Typography>
            )}
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Notifications notifications={notifications} />
          <UserBadges badges={userBadges} />
          <Paper style={{ padding: '1rem', marginTop: '1rem' }}>
            <Typography variant="h6" gutterBottom>Recommendations</Typography>
            {recommendations.length > 0 ? (
              <List>
                {recommendations.map((material) => (
                  <ListItem key={material.id}>
                    <ListItemText 
                      primary={material.title}
                      secondary={
                        <>
                          <Typography component="span" variant="body2" color="textPrimary">
                            Difficulty: {material.difficulty_level}
                          </Typography>
                          <br />
                          <Typography component="span" variant="body2" color="textSecondary">
                            {material.description}
                          </Typography>
                        </>
                      }
                    />
                    <Button 
                      variant="contained" 
                      color="primary" 
                      onClick={() => handleStartLearning(material.id)}
                    >
                      Start
                    </Button>
                  </ListItem>
                ))}
              </List>
            ) : (
              <Typography>No recommendations available at the moment.</Typography>
            )}
          </Paper>
        </Grid>
      </Grid>
      <LearningMaterialSearch onSearch={handleSearch} />
      {searchResults.length > 0 && (
        <Grid item xs={12}>
          <Paper style={{ padding: '1rem' }}>
            <Typography variant="h6" gutterBottom>Search Results</Typography>
            <List>
              {searchResults.map((material) => (
                <ListItem key={material.id}>
                  <ListItemText
                    primary={material.title}
                    secondary={material.description}
                  />
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={() => handleStartLearning(material.id)}
                  >
                    Start
                  </Button>
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
      )}
    </Container>
  );
};

export default Dashboard;
