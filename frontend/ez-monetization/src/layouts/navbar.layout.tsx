/**
 * Renders a layout with a navbar and a main content area.
 * @param {Object} props - The component props.
 * @param {React.ReactNode} props.children - The child components to render within the main content area.
 * @returns {React.ReactNode} The rendered layout.
 */
import Navbar from "../components/navbar.component";
import { Box } from "@mui/material";

export default function NavbarLayout({ children }) {
  return (
    <>
      <Navbar />
      <Box component="main" sx={{ pt: 8, pb: 6 }}>
        {/* pt (padding-top) value depends on Navbar's height */}
        {children}
      </Box>
    </>
  );
}