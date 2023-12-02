// Sidebar.tsx
import { Button, Drawer, Grid, Typography, IconButton } from "@mui/material";
import DashboardIcon from "@mui/icons-material/Dashboard";
import NotificationsNoneIcon from "@mui/icons-material/NotificationsNone";
import SettingsIcon from "@mui/icons-material/Settings";

const Sidebar: React.FC = () => {
  return (
    <Drawer
      variant="permanent"
      anchor="left"
      sx={{
        width: 261,
        flexShrink: 0,
        gap: 64,
        // "& .MuiDrawer-paper": {
        //   width: 261,
        //   boxSizing: "border-box",
        // },
      }}
    >
      <Grid
        container
        direction="column"
        justifyContent="space-between"
        alignItems="center"
        sx={{
          padding: "24px",
          gap: "16px",
        }}
      >
        <Grid item>
          <img
            src="../../public/man_4140048.png"
            alt="Logo"
            style={{ width: "70%", maxWidth: "70%", height: "auto" }}
          />
        </Grid>
        <Grid
          item
          container
          direction="column"
          alignItems="center"
          sx={{ gap: "8px" }}
        >
          <Typography
            variant="h3"
            component="h3"
            color="primary"
          >
            Tushar Sadana
          </Typography>
          <Button
            variant="outlined"
            color="secondary"
            sx={{
              borderRadius: "29px",
              width: "80px",
            }}
          >
            Edit
          </Button>
        </Grid>
      </Grid>
      <Grid
        container
        direction="column"
        justifyContent="space-between"
        alignItems="center"
        sx={{
          padding: "24px",
          gap: "24px",
        }}
      >
        <IconButton color="primary" sx={{ width: 175, gap: 1 }}>
          <DashboardIcon />
          <Typography variant="body2">
            Dashboard
          </Typography>
        </IconButton>
        <IconButton color="primary" sx={{ width: 175, gap: 1 }}>
          <NotificationsNoneIcon />
          <Typography variant="body2">
            Notifications
          </Typography>
        </IconButton>
        <IconButton color="primary" sx={{ width: 175, gap: 1 }}>
          <SettingsIcon />
          <Typography variant="body2">
            Account Settings
          </Typography>
        </IconButton>
      </Grid>
    </Drawer>
  );
};

export default Sidebar;
