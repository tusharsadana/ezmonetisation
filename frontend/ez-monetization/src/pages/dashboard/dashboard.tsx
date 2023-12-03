import React from 'react';
import Sidebar from '../../components/sidebar/sidebar.component';
import Appbar from '../../components/appbar.component';
import { Grid } from '@mui/material';

const Dashboard: React.FC = () => {
    return (
        <Grid>
            {/* <Appbar /> */}
            <Sidebar />
        </Grid>
    );
};

export default Dashboard;