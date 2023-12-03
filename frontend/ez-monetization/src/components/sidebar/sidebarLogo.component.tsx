import { Grid } from "@mui/material";

const SidebarLogo: React.FC = () => {
  return (
    <Grid
      container
      direction="row"
      justifyContent="center"
      alignItems="center"
      sx={{ marginTop: "20px" }}
    >
      <img
        src="../../../public/Socially- 28-11-2023.png"
        alt="Logo"
        style={{ width: "90%", height: "90%" }}
      />
    </Grid>
  );
};

export default SidebarLogo;
