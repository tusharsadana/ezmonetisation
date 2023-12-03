import { Box, Grid } from "@mui/material";
import { drawerWidth } from "./sidebar.component";

const SidebarLogo: React.FC = () => {
  return (
    <Grid
      container
      justifyContent="center"
      alignItems="center"
      sx={{ marginTop: "20px" }}
    >
      <Box
        component="img"
        src="src/assets/logo.png"
        alt="Logo"
        sx={{
          width: { xs: '80%', sm: '60%', md: '60%', lg: '60%' },
          maxWidth: drawerWidth, // Maximum logo width
          height: 'auto',
          objectFit: 'contain'
        }}
      />
    </Grid>
  );
};

export default SidebarLogo;
