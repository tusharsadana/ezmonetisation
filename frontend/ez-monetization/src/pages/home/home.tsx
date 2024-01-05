import React from 'react';
import Sidebar, { drawerOpen } from '../../components/sidebar/sidebar.component';
import { Outlet } from 'react-router-dom';
import { AppBar, Box, IconButton, Toolbar, useMediaQuery } from '@mui/material';
import theme from '../../theme/ThemeProvider';
import MenuIcon from '@mui/icons-material/Menu';

const Home: React.FC = () => {
    const isMobile = useMediaQuery(theme.breakpoints.down("sm"));

    return (
        <>
            {/* <Appbar /> */}
            <Box sx={{ display: 'flex', width: "100%"}}>
                <Sidebar />
                <Box
                    sx={{
                        flexGrow: 1, p: 3, width: { sm: `calc(100% - ${240}px)`},
                        overflow: 'auto'
                    }}
                >
                    {isMobile && <AppBar position="fixed" color="default" elevation={0} sx={{ backgroundColor: theme.palette.background.paper }}>
                        <Toolbar>
                            <IconButton
                                edge="start"
                                color="inherit"
                                aria-label="menu"
                                sx={{ m: 2, boxShadow: 0, outline: 0 }}
                                onClick={() => drawerOpen.value = !drawerOpen.value}
                            >
                                <MenuIcon />
                            </IconButton>
                            {/* Other toolbar items can be added here */}
                        </Toolbar>
                    </AppBar>}
                    <Box sx={{ marginTop: 2 }}>
                        <Outlet /> {/* Main content will be rendered here */}
                    </Box>
                </Box>
            </Box>

        </>
    );
};

export default Home;