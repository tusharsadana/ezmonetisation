import { Grid, Typography, MenuItem, Paper } from "@mui/material";
import DashboardIcon from "@mui/icons-material/Dashboard";
import HourglassEmptyIcon from "@mui/icons-material/HourglassEmpty";
import SubscriptionsIcon from "@mui/icons-material/Subscriptions";
import { useNavigate } from "react-router-dom";

const SidebarMenu: React.FC = () => {
  const navigate = useNavigate();
  return (

    <Paper elevation={0} sx={{ maxWidth: 300, margin: 'auto', marginTop: 4 }}>
      <Grid
        container
        direction="column"
        justifyContent="flex-start"
        alignItems="flex-start"
        sx={{
          padding: 3,
          gap: "16px",
        }}
      >
        {[{
          label: "Dashboard",
          Icon: DashboardIcon,
          path: "/",
        }, {
          label: "Watch hours",
          Icon: HourglassEmptyIcon,
          path: "/watch",
        }, {
          label: "Subscribers",
          Icon: SubscriptionsIcon,
          path: "/sub",
        }].map((item, index) => (
          <MenuItem
            key={index}
            onClick={() => navigate(item.path)}
            sx={{
              display: "flex",
              alignItems: "center",
              cursor: "pointer",
              borderRadius: 2,
              boxShadow: 1,
              "&:hover": {
                backgroundColor: "#5569ff",
                color: "white",
                boxShadow: 3,
              },
              width: '100%', // Make menu items full width
              padding: 2,
            }}
          >
            <item.Icon sx={{ marginRight: 2 }} />
            <Typography variant="h6" component="h6">
              {item.label}
            </Typography>
          </MenuItem>
        ))}
      </Grid>
    </Paper>
  );
};

export default SidebarMenu;

