import { Grid, Typography, MenuItem, Paper } from "@mui/material";
import DashboardIcon from "@mui/icons-material/Dashboard";
import HourglassEmptyIcon from "@mui/icons-material/HourglassEmpty";
import SubscriptionsIcon from "@mui/icons-material/Subscriptions";
import LogoutIcon from '@mui/icons-material/Logout';
import { useNavigate } from "react-router-dom";
import { signal } from "@preact/signals-react";
import Cookies from "universal-cookie";
import { AuthContext } from "../../contexts/auth.context";
import { useContext } from "react";

const selectedMenuItem = signal(0);
const SidebarMenu: React.FC = () => {
  const navigate = useNavigate();
  const { logout } = useContext(AuthContext);

  const cookie = new Cookies();
  const menuItems = [
    {
      label: "Dashboard",
      Icon: DashboardIcon,
      path: "/",
    },
    {
      label: "Watch hours",
      Icon: HourglassEmptyIcon,
      path: "/watch",
    },
    {
      label: "Subscribers",
      Icon: SubscriptionsIcon,
      path: "/sub",
    },
    {
      label: "Logout",
      Icon: LogoutIcon,
      path: "/login",
    }
  ];
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
        {menuItems.map((item, index) => (
          <MenuItem
            key={index}
            onClick={() => {
              selectedMenuItem.value = index;
              if(item.label === "Logout")
              {
                logout();
                selectedMenuItem.value = 0;
              }
              navigate(item.path);
            }}
            sx={{
              display: "flex",
              alignItems: "center",
              cursor: "pointer",
              borderRadius: 2,
              boxShadow: 1,
              backgroundColor: selectedMenuItem.value === index ? "#5569ff" : "inherit",
              color: selectedMenuItem.value === index ? "white" : "inherit",
              "&:hover": {
                backgroundColor: "#5569ff",
                color: "white",
                boxShadow: 3,
              },
              width: '100%',
              padding: 1.5,
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

