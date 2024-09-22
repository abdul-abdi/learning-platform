import React, { useState, useEffect } from 'react';
import { List, ListItem, ListItemText, Typography, Paper, TextField, Button } from '@material-ui/core';
import { getForumPosts, createForumPost } from '../../services/api';

const ForumPosts = ({ materialId }) => {
  const [posts, setPosts] = useState([]);
  const [newPost, setNewPost] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchPosts();
  }, [materialId]);

  const fetchPosts = async () => {
    try {
      const response = await getForumPosts(materialId);
      setPosts(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to load forum posts');
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createForumPost(materialId, { content: newPost });
      setNewPost('');
      fetchPosts();
    } catch (err) {
      setError('Failed to create post');
    }
  };

  if (loading) return <Typography>Loading forum posts...</Typography>;
  if (error) return <Typography color="error">{error}</Typography>;

  return (
    <Paper style={{ padding: '1rem', marginTop: '1rem' }}>
      <Typography variant="h6" gutterBottom>Discussion Forum</Typography>
      <List>
        {posts.map((post) => (
          <ListItem key={post.id}>
            <ListItemText
              primary={post.content}
              secondary={`${post.user.username} - ${new Date(post.created_at).toLocaleString()}`}
            />
          </ListItem>
        ))}
      </List>
      <form onSubmit={handleSubmit}>
        <TextField
          fullWidth
          multiline
          rows={3}
          variant="outlined"
          label="New post"
          value={newPost}
          onChange={(e) => setNewPost(e.target.value)}
          style={{ marginBottom: '1rem' }}
        />
        <Button type="submit" variant="contained" color="primary">
          Submit Post
        </Button>
      </form>
    </Paper>
  );
};

export default ForumPosts;