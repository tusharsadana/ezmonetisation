import React, { FormEvent, useEffect, useState } from "react";
import {
    Avatar,
    Box,
    Button,
    Checkbox,
    Container,
    CssBaseline,
    FormControlLabel,
    Grid,
    Paper,
    TextField,
    ThemeProvider,
    Typography,
    useMediaQuery,
} from "@mui/material";
import { createTheme } from "@mui/material/styles";
import { useNavigate, Link } from "react-router-dom";
import { LockOutlined } from "@mui/icons-material";
import { signUp } from "../../services/auth.service";
import { ISignUp } from "../../models/auth.model";
import theme from "../../theme/ThemeProvider";
import { toast } from "react-toastify";
import { useSignal } from "@preact/signals-react";

export default function Signup(): JSX.Element {
    const [inputState, setInputState] = useState<ISignUp>({
        username: "",
        password: "",
        first_name: "",
        last_name: "",
    });

    const checkedSignal = useSignal(false);
    const navigate = useNavigate();

    function handleInput(event: React.ChangeEvent<HTMLInputElement>) {
        setInputState({
            ...inputState,
            [event.target.name]: event.target.value,
        });
    }


    function handleRegistration(): void {
        const { username, password, first_name, last_name } = inputState;
        if (username === "" || password === "" || first_name === "" || last_name === "") {
            toast.error("Please fill in all fields");
            return;
        }

        if (!checkedSignal.value) {
            toast.error("Please accept the Terms and Conditions");
            return;
        }

        let payload = {
            username: username,
            password: password,
            confirm_password: password,
            first_name: first_name,
            last_name: last_name,
        };

        signUp(payload);
    }

    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

    const signUpBox = <Box
        sx={{
            marginTop: 4,
            marginBottom: 4,
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
                p={isMobile ? -2 : 4}
                component={Paper}
                elevation={0}
                square
                sx={{
                    borderTopRightRadius: '16px', // Set the top-right border-radius
                    borderBottomRightRadius: '16px',
                    borderBottomLeftRadius: isMobile ? '16px' : '0px',
                    borderTopLeftRadius: isMobile ? '16px' : '0px', // Set the bottom-right border-radius
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

                    <Typography component="h1" variant="h3">
                        Sign Up
                    </Typography>
                    <Typography component={"p"} fontWeight={"light"}>
                        Fill in the fields below to sign up for an account.
                    </Typography>
                    <Box
                        component="form"
                        noValidate
                        onSubmit={(e) => { e.preventDefault(); }}
                        sx={{ mt: 3 }}
                    >
                        <Grid container spacing={2}>
                            <Grid item xs={12} sm={6}>
                                <TextField
                                    autoComplete="given-name"
                                    name="first_name"
                                    required
                                    fullWidth
                                    id="first_name"
                                    label="First Name"
                                    autoFocus
                                    onChange={handleInput}
                                />
                            </Grid>
                            <Grid item xs={12} sm={6}>
                                <TextField
                                    required
                                    fullWidth
                                    id="last_name"
                                    label="Last Name"
                                    name="last_name"
                                    autoComplete="family-name"
                                    onChange={handleInput}

                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    required
                                    fullWidth
                                    id="username"
                                    label="Email Address"
                                    name="username"
                                    autoComplete="email"
                                    onChange={handleInput}

                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    required
                                    fullWidth
                                    name="password"
                                    label="Password"
                                    type="password"
                                    id="password"
                                    autoComplete="new-password"
                                    onChange={handleInput}

                                />
                            </Grid>
                            <Grid item xs={12}>
                                <FormControlLabel
                                    control={<Checkbox value="remember" color="primary" onChange={(e) => { checkedSignal.value = e.target.checked }} />}
                                    label="I accept the Terms and Conditions"

                                />
                            </Grid>
                        </Grid>
                        <Button
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                            onClick={handleRegistration}
                        >
                            Sign Up
                        </Button>
                        <Grid item xs={12} md={12} mt={2} >
                            <Link to="/login" style={{ textDecoration: 'none' }}>
                                <Button variant="outlined" color="secondary" sx={{
                                    boxShadow: 'none', // Disable the default box-shadow
                                    fontSize: '10px', // Larger font size
                                    textTransform: 'none', // Prevent uppercase transform
                                }}>
                                    Already have an account? Sign In.
                                </Button>
                            </Link>
                        </Grid>
                    </Box>
                </Box>
            </Grid>
        </Grid>
    </Box>

    return (
        <>
            {isMobile ? (<Container component="main" maxWidth={"xl"}>
                {signUpBox}
            </Container>) : (signUpBox)}
        </>
    );
}