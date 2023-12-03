// Sidebar.tsx
import { Drawer, useMediaQuery, MenuItem } from "@mui/material";
import SidebarProfile from "./sidebarProfile.component";
import SidebarMenu from "./sidebarMenu.component";
import SidebarLogo from "./sidebarLogo.component";
import { useSignal } from "@preact/signals-react";
import theme from "../../theme/ThemeProvider";
import MenuIcon from "@mui/icons-material/Menu";
import CloseIcon from "@mui/icons-material/Close";

const Sidebar: React.FC = () => {
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));
  const drawerOpen = useSignal(true);

  const handleDrawerToggle = () => {
    drawerOpen.value = !drawerOpen.value;
  };

  return (
    <>
      {isMobile ? (
        <>
          <MenuItem
            onClick={handleDrawerToggle}
            sx={{ display: { sm: "block", md: "none" }, cursor: "pointer" }}
          >
            {drawerOpen.value ? <CloseIcon /> : <MenuIcon />}
          </MenuItem>
          <Drawer
            variant="temporary"
            open={drawerOpen.value}
            onClose={() => (drawerOpen.value = false)}
            anchor="left"
            sx={{
              width: 261,
              flexShrink: 0,
              gap: 64,
              "& .MuiDrawer-paper": {
                width: 261,
                boxSizing: "border-box",
              },
            }}
          >
            <MenuItem
              onClick={handleDrawerToggle}
              sx={{
                position: "absolute",
                top: 0,
                right: 0,
                m: 0,
                cursor: "pointer",
              }}
            >
              {drawerOpen.value ? <CloseIcon /> : <MenuIcon />}
            </MenuItem>
            <SidebarLogo />
            <SidebarProfile />
            <SidebarMenu />
          </Drawer>
        </>
      ) : (
        <>
          <MenuItem
            onClick={handleDrawerToggle}
            sx={{ display: { sm: "block", md: "none" }, cursor: "pointer" }}
          >
            {drawerOpen.value ? <CloseIcon /> : <MenuIcon />}
          </MenuItem>
          <Drawer
            variant="temporary"
            open={drawerOpen.value}
            onClose={() => (drawerOpen.value = false)}
            sx={{
              flexShrink: 0,
              gap: 64,
              "& .MuiDrawer-paper": {
                width: 261,
                boxSizing: "border-box",
              },
            }}
          >
            <MenuItem
              onClick={handleDrawerToggle}
              sx={{
                position: "absolute",
                top: 0,
                left: 0,
                m: 0,
                cursor: "pointer",
              }}
            >
              {drawerOpen.value ? <CloseIcon /> : <MenuIcon />}
            </MenuItem>
            <SidebarLogo />
            <SidebarProfile />
            <SidebarMenu />
          </Drawer>
        </>
      )}
    </>
  );
};

export default Sidebar;
