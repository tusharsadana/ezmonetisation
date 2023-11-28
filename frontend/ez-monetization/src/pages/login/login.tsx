import { useState, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
    Box,
    Button,
    Checkbox,
    Container,
    CssBaseline,
    FormControlLabel,
    Grid,
    Paper,
    TextField,
    Typography,
} from "@mui/material";
import { signIn } from "../../services/auth.service";
import { AuthContext } from "../../contexts/auth.context";
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


    const handleChange = (event: { target: { name: any; value: any; }; }) => {
        setInputState({ ...inputState, [event.target.name]: event.target.value });

    };

    const handleLogin = () => {
        signIn(email, password)
            .then((res) => {
                console.log(res)
                login(res.access, res.refresh);
                toast.success("Logged in successfully");
            })
            .catch((err) => {
                console.log(err);
                toast.error("Login failed");
            });
    };


    return (
        <>
            <Container component="main" maxWidth="lg">
                <Box
                    sx={{
                        marginTop: 8,
                    }}
                >
                    <Grid container>
                        <CssBaseline />
                        <Grid
                            item
                            xs={false}
                            sm={4}
                            md={6}
                            sx={{
                                backgroundImage: "url(https://source.unsplash.com/random)",
                                backgroundRepeat: "no-repeat",
                                backgroundColor: (t) =>
                                    t.palette.mode === "light"
                                        ? t.palette.grey[50]
                                        : t.palette.grey[900],
                                backgroundSize: "cover",
                                backgroundPosition: "center",
                                borderRadius: "16px 0 0 16px",
                            }}
                        />
                        <Grid
                            item
                            xs={12}
                            sm={8}
                            md={6}
                            p={4}
                            component={Paper}
                            elevation={0}
                            square
                            sx={{
                                borderTopRightRadius: '16px', // Set the top-right border-radius
                                borderBottomRightRadius: '16px', // Set the bottom-right border-radius
                            }}
                        >
                            <Box
                                sx={{
                                    my: 8,
                                    mx: 4,
                                    display: "flex",
                                    flexDirection: "column",
                                    alignItems: "center",
                                }}
                            >
                                <Typography component="h1" variant="h3" >
                                    Sign in
                                </Typography>
                                <Typography component={"p"} fontWeight={"light"}>
                                    Fill in the fields below to login to your account
                                </Typography>
                                <Box
                                    component="form"
                                    noValidate
                                    onSubmit={(e) => { e.preventDefault(); }}
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
                                        onChange={handleChange}
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
                                        onChange={handleChange}
                                    />
                                    <FormControlLabel
                                        control={<Checkbox value="remember" color="primary" />}
                                        label="Remember me"

                                    />
                                    <Button
                                        type="submit"
                                        fullWidth
                                        variant="contained"
                                        sx={{ mt: 3, mb: 2 }}
                                        onClick={handleLogin}
                                    >
                                        Sign In
                                    </Button>
                                    <Grid container>
                                        <Grid item xs>
                                            <Link to="/signup" style={{ textDecoration: 'none' }}>
                                                <Button variant="outlined" color="secondary" sx={{
                                                    boxShadow: 'none', // Disable the default box-shadow
                                                    fontSize: '10px', // Larger font size
                                                    textTransform: 'none', // Prevent uppercase transform
                                                }}>
                                                    Forgot Password?
                                                </Button>
                                            </Link>
                                        </Grid>
                                        <Grid item xs>
                                            <Link to="/signup" style={{ textDecoration: 'none' }}>
                                                <Button variant="outlined" color="secondary" sx={{
                                                    boxShadow: 'none', // Disable the default box-shadow
                                                    fontSize: '10px', // Larger font size
                                                    textTransform: 'none', // Prevent uppercase transform
                                                }}>
                                                    Don't have an account?
                                                </Button>
                                            </Link>
                                        </Grid>
                                    </Grid>
                                </Box>
                            </Box>
                        </Grid>
                    </Grid>
                </Box>
            </Container>
        </>
    );
}