import { Grid, Paper, Typography } from '@mui/material';
import React from 'react';

const Dashboard: React.FC = () => {
    return (
        <>
            <Typography variant="h4" component="h4" gutterBottom align="left">
                Dashboard
            </Typography>
            <Grid container spacing={2} justifyContent="flex-start">
                {[1, 2, 3, 4, 5].map((item) => (
                    <Grid item xs={12} sm={6} md={4} key={item}>
                        <Paper sx={{ padding: 2, textAlign: 'left' }}>
                            <Typography variant="h6" align="left">Item {item}</Typography>
                            <Typography align="left">Some description for item {item}.</Typography>
                        </Paper>
                    </Grid>
                ))}
            </Grid>
        </>
    );
};

export default Dashboard;
