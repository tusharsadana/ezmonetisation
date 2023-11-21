import React, { FormEvent, useEffect, useState } from "react";
import { registerUser } from "../services/auth";
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
import { createTheme } from "@mui/material/styles";
import { useNavigate, Link } from "react-router-dom";
import { LockOutlined } from "@mui/icons-material";
import { signUp } from "../models/auth.model";

export default function Signup(): JSX.Element {
  const [inputState, setInputState] = useState<signUp>({
    username: "",
    password: "",
    confirm_password: "",
    first_name: "",
    last_name: "",
  });

  const [isDisabled, setIsDisabled] = useState<boolean>(true);

  const { username, password, confirm_password, first_name, last_name } =
    inputState;
  const navigate = useNavigate();
  const defaultTheme = createTheme();

  function handleInput(event: React.ChangeEvent<HTMLInputElement>) {
    setInputState({
      ...inputState,
      [event.target.name]: event.target.value,
    });
  }

  useEffect(() => {
    if (
      username === "" ||
      password === "" ||
      confirm_password === "" ||
      first_name === "" ||
      last_name === ""
    ) {
      setIsDisabled(true);
    }
    if (password === confirm_password) {
      setIsDisabled(false);
    } else {
      setIsDisabled(true);
    }
  }, [
    password,
    confirm_password,
    username,
    first_name,
    last_name,
    handleInput,
  ]);

  function handleRegistration(): void {
    const { username, password, first_name, last_name } = inputState;
    let payload = {
      username: username,
      password: password,
      first_name: first_name,
      last_name: last_name,
    };
    registerUser(payload);
    console.log(payload);
  }

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
            Sign up
          </Typography>
          <Box
            component="form"
            noValidate
            onSubmit={handleRegistration}
            sx={{ mt: 3 }}
          >
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  autoComplete="given-name"
                  name="firstName"
                  required
                  fullWidth
                  id="firstName"
                  label="First Name"
                  autoFocus
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  required
                  fullWidth
                  id="lastName"
                  label="Last Name"
                  name="lastName"
                  autoComplete="family-name"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  id="email"
                  label="Email Address"
                  name="email"
                  autoComplete="email"
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
                />
              </Grid>
            </Grid>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              disabled={isDisabled}
            >
              Sign Up
            </Button>
            <Grid container justifyContent="flex-end">
              <Grid item>
                <Link to="/login">Already have an account? Sign in</Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}
