import {
  Avatar,
  Button,
  Grid,
  Paper,
  Typography,
} from "@mui/material";
import { drawerWidth } from "./sidebar.component";
import Cookies from "universal-cookie";
import { FIRST_NAME } from "../../contexts/auth.context";

const SidebarProfile: React.FC = () => {
  const cookie = new Cookies();
  const username = cookie.get(FIRST_NAME);
  return (
    <Paper elevation={0} sx={{ maxWidth: drawerWidth, marginTop: 2, textAlign: 'center' }}>
      <Grid
        container
        direction="column"
        justifyContent="center"
        alignItems="center"
        sx={{ gap: 1 }}
      >
        <Avatar
          src="../../public/man_4140048.png"
          alt="Logo"
          sx={{ width: 80, height: 80, marginBottom: 1 }}
        />
        <Typography variant="h6" component="h6" color="primary" sx={{ fontWeight: 'bold' }}>
          Hi, {username}
        </Typography>
        <Button
          variant="outlined"
          color="secondary"
          size="small"
          sx={{
            borderRadius: 20,
            textTransform: 'none',
            fontSize: '0.7rem',
            padding: '4px 10px',
            boxShadow: 'none',
            marginTop: 1,
          }}
        >
          Edit
        </Button>
      </Grid>
    </Paper>
  );
};

export default SidebarProfile;
