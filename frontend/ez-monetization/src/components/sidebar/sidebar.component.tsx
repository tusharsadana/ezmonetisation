// Sidebar.tsx
import { Drawer, useMediaQuery, MenuItem } from "@mui/material";
import SidebarProfile from "./sidebar-profile.component";
import SidebarMenu from "./sidebar-menu.component";
import SidebarLogo from "./sidebar-logo.component";
import { signal } from "@preact/signals-react";
import theme from "../../theme/ThemeProvider";
import CloseIcon from "@mui/icons-material/Close";

export const drawerWidth = 240;


export const drawerOpen = signal(true);

const Sidebar: React.FC = () => {
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));


  const handleDrawerToggle = () => {
    drawerOpen.value = !drawerOpen.value;
  };

  return (
    <>

      <Drawer
        variant={isMobile ? "temporary" : "permanent"}
        open={drawerOpen.value}
        onClose={() => (drawerOpen.value = false)}
        sx={{
          flexShrink: 0,
          width: drawerWidth,
          "& .MuiDrawer-paper": {
            width: drawerWidth,
            boxSizing: "border-box",
          },
        }}
      >
        <MenuItem
          onClick={handleDrawerToggle}
          sx={{
            display: isMobile ? "flex" : 'none',
            justifyContent: "flex-end",
            boxShadow: "none",
            "&:hover": {
              backgroundColor: "transparent",
              color: "black",
            },

          }}
        >
          <CloseIcon />
        </MenuItem>
        <SidebarLogo />
        <SidebarProfile />
        <SidebarMenu />
      </Drawer>

    </>


  );
};

export default Sidebar;
