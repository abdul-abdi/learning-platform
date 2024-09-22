import React, { useState } from 'react';
import { TextField, Button, Grid } from '@material-ui/core';

const LearningMaterialSearch = ({ onSearch }) => {
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = (e) => {
    e.preventDefault();
    onSearch(searchQuery);
  };

  return (
    <form onSubmit={handleSearch}>
      <Grid container spacing={2} alignItems="center">
        <Grid item xs={9}>
          <TextField
            fullWidth
            variant="outlined"
            label="Search learning materials"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </Grid>
        <Grid item xs={3}>
          <Button fullWidth variant="contained" color="primary" type="submit">
            Search
          </Button>
        </Grid>
      </Grid>
    </form>
  );
};

export default LearningMaterialSearch;