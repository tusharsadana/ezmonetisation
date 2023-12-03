// Navbar.tsx
import React, { useState } from 'react';
import { AppBar, Toolbar, Menu, MenuItem } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';

const Appbar: React.FC = () => {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <AppBar
      position="fixed"
      style={{ backgroundColor: 'transparent', boxShadow: 'none' }}
    >
      <Toolbar>
        <div
          onClick={handleClick}
          style={{ cursor: 'pointer', marginRight: '16px' }}
        >
          <MenuIcon style={{color:'black'}} />
        </div>
      </Toolbar>
    </AppBar>
  );
};

export default Appbar;
