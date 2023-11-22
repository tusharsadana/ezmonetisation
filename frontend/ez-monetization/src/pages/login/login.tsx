import { useState, useEffect, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
    Avatar,
    Box,
    Button,
    Container,
    CssBaseline,
    Grid,
    TextField,
    ThemeProvider,
    Typography,
} from "@mui/material";
import { LockOutlined } from "@mui/icons-material";
import { signIn } from "../../services/auth.service";
import { AuthContext } from "../../contexts/auth.context";
import { createTheme } from "@mui/material/styles";
import { ISignIn } from "../../models/auth.model";
import { toast } from "react-toastify";

export default function Login(): JSX.Element {
    const [inputState, setInputState] = useState<ISignIn>({
        email: "",
        password: "",
    });

    const { email, password } = inputState;
    const navigate = useNavigate();
    const { login } = useContext(AuthContext);

    const handleLogin = () => {
        signIn(email, password)
            .then((res) => {
                login(res.access, res.refresh);
                toast.success("Logged in successfully");
            })
            .catch((err) => {
                console.log(err);
                toast.error("Login failed");
            });
    };

    const defaultTheme = createTheme();

    return (
        <ThemeProvider theme={defaultTheme}>
            <Container component="main" maxWidth="xs">
                <CssBaseline />
                <Box
                    sx={{
                        marginTop: 8,
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "center",
                    }}
                >
                    <Avatar sx={{ m: 1, bgcolor: "secondary.main" }}>
                        <LockOutlined />
                    </Avatar>
                    <Typography component="h1" variant="h5">
                        Sign in
                    </Typography>
                    <Box
                        component="form"
                        onSubmit={handleLogin}
                        noValidate
                        sx={{ mt: 1 }}
                    >
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            id="email"
                            label="Email Address"
                            name="email"
                            autoComplete="email"
                            autoFocus
                        />
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            name="password"
                            label="Password"
                            type="password"
                            id="password"
                            autoComplete="current-password"
                        />
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                        >
                            Sign In
                        </Button>
                        <Grid container>
                            <Grid item xs>
                                <Link to="#">Forgot password?</Link>
                            </Grid>
                            <Grid item>
                                <Link to="/signup">{"Don't have an account? Sign Up"}</Link>
                            </Grid>
                        </Grid>
                    </Box>
                </Box>
            </Container>
        </ThemeProvider>
    );
}