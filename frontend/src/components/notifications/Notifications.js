import React from 'react';
import { Typography, Paper, List, ListItem, ListItemText, IconButton } from '@material-ui/core';
import { Close as CloseIcon } from '@material-ui/icons';
import { markNotificationAsRead } from '../../services/api';

const Notifications = ({ notifications }) => {
  const handleMarkAsRead = async (notificationId) => {
    try {
      await markNotificationAsRead(notificationId);
      // Update the notifications list in the parent component
    } catch (error) {
      console.error('Error marking notification as read:', error);
    }
  };

  return (
    <Paper style={{ padding: '1rem', marginBottom: '1rem' }}>
      <Typography variant="h6" gutterBottom>Notifications</Typography>
      <List>
        {notifications.map(notification => (
          <ListItem key={notification.id}>
            <ListItemText primary={notification.message} secondary={new Date(notification.created_at).toLocaleString()} />
            <IconButton edge="end" aria-label="mark as read" onClick={() => handleMarkAsRead(notification.id)}>
              <CloseIcon />
            </IconButton>
          </ListItem>
        ))}
      </List>
    </Paper>
  );
};

export default Notifications;