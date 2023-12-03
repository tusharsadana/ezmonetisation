import { Grid, Typography, MenuItem } from "@mui/material";
import DashboardIcon from "@mui/icons-material/Dashboard";
import HourglassEmptyIcon from "@mui/icons-material/HourglassEmpty";
import SubscriptionsIcon from "@mui/icons-material/Subscriptions";
import { useNavigate } from "react-router-dom";

const SidebarMenu: React.FC = () => {
  const navigate = useNavigate();
  return (
    <Grid
      container
      direction="column"
      justifyContent="space-between"
      alignItems="flex-start"
      sx={{
        padding: "24px",
        gap: "24px",
      }}
    >
      <MenuItem
        onClick={() => {
          navigate("/");
        }}
        sx={{
          gap: 1,
          display: "flex",
          alignItems: "center",
          cursor: "pointer",
          boxShadow: "none",
          "&:hover": {
            backgroundColor: "#5569ff",
            color: "white",
          },
        }}
      >
        <DashboardIcon />
        <Typography variant="h5" component="h5" sx={{ marginLeft: 2 }}>
          Dashboard
        </Typography>
      </MenuItem>
      <MenuItem
        onClick={() => {
          navigate("/watching");
        }}
        sx={{
          gap: 1,
          display: "flex",
          alignItems: "center",
          cursor: "pointer",
          boxShadow: "none",
          "&:hover": {
            backgroundColor: "#5569ff",
            color: "white",
          },
        }}
      >
        <HourglassEmptyIcon />
        <Typography variant="h5" component="h5" sx={{ marginLeft: 2 }}>
          Watch hours
        </Typography>
      </MenuItem>
      <MenuItem
        onClick={() => {
          navigate("/subscribers");
        }}
        sx={{
          gap: 1,
          display: "flex",
          alignItems: "center",
          cursor: "pointer",
          boxShadow: "none",
          "&:hover": {
            backgroundColor: "#5569ff",
            color: "white",
          },
        }}
      >
        <SubscriptionsIcon />
        <Typography variant="h5" component="h5" sx={{ marginLeft: 2 }}>
          Subscribers
        </Typography>
      </MenuItem>
    </Grid>
  );
};

export default SidebarMenu;
