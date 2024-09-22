import React from 'react';
import { Container, Typography, Button, Grid } from '@material-ui/core';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <Container maxWidth="md" style={{ marginTop: '2rem' }}>
      <Grid container spacing={4} alignItems="center">
        <Grid item xs={12} md={6}>
          <Typography variant="h2" component="h1" gutterBottom>
            Welcome to AI-Driven Learning
          </Typography>
          <Typography variant="h5" paragraph>
            Personalized learning paths, adaptive content, and AI-powered recommendations to help you achieve your learning goals.
          </Typography>
          <Button variant="contained" color="primary" component={Link} to="/register" size="large">
            Get Started
          </Button>
        </Grid>
        <Grid item xs={12} md={6}>
          {/* Add an illustration or image here */}
        </Grid>
      </Grid>
    </Container>
  );
};

export default Home;
