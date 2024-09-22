import React from 'react';
import { Typography, Paper, Grid, Avatar } from '@material-ui/core';

const UserBadges = ({ badges }) => {
  return (
    <Paper style={{ padding: '1rem', marginTop: '1rem' }}>
      <Typography variant="h6" gutterBottom>Your Badges</Typography>
      <Grid container spacing={2}>
        {badges.map(badge => (
          <Grid item key={badge.id} xs={4}>
            <Avatar alt={badge.name} src={badge.image_url} />
            <Typography variant="body2">{badge.name}</Typography>
          </Grid>
        ))}
      </Grid>
    </Paper>
  );
};

export default UserBadges;