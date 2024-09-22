import React from 'react';
import { Typography, Paper, Grid } from '@material-ui/core';

const UserStatistics = ({ userProgress }) => {
  const completedMaterials = userProgress.items.filter(item => item.status === 'completed').length;
  const inProgressMaterials = userProgress.items.filter(item => item.status === 'in_progress').length;
  const totalMaterials = userProgress.total;

  return (
    <Paper style={{ padding: '1rem', marginBottom: '1rem' }}>
      <Typography variant="h6" gutterBottom>Learning Statistics</Typography>
      <Grid container spacing={2}>
        <Grid item xs={4}>
          <Typography variant="body1">Completed: {completedMaterials}</Typography>
        </Grid>
        <Grid item xs={4}>
          <Typography variant="body1">In Progress: {inProgressMaterials}</Typography>
        </Grid>
        <Grid item xs={4}>
          <Typography variant="body1">Total: {totalMaterials}</Typography>
        </Grid>
      </Grid>
    </Paper>
  );
};

export default UserStatistics;