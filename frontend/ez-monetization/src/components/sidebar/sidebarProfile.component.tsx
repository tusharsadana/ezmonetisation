import {
  Button,
  Grid,
  Typography,
} from "@mui/material";

const SidebarProfile: React.FC = () => {
  return (
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
        <Grid container direction="row" alignItems="center" gap={2}>
          <img
            src="../../public/man_4140048.png"
            alt="Logo"
            style={{ width: "40px", height: "auto" }}
          />
          <Typography
            variant="h5"
            component="h5"
            color="primary"
            sx={{ textAlign: "center" }}
          >
            Tushar Sadana
          </Typography>
        </Grid>
      </Grid>
      <Grid
        item
        container
        direction="column"
        alignItems="center"
        sx={{ gap: "6px" }}
      >
        <Button
          variant="outlined"
          color="secondary"
          size="small"
          sx={{
            borderRadius: "29px",
            boxShadow: "none",
          }}
        >
          Edit
        </Button>
      </Grid>
    </Grid>
  );
};

export default SidebarProfile;
