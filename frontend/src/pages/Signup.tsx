import React, { FormEvent, useEffect, useState } from "react";
import { registerUser } from "../services/auth";
import {
  Avatar,
  Box,
  Button,
  Container,
  CssBaseline,
  Grid,
  IconButton,
  InputAdornment,
  TextField,
  ThemeProvider,
  Typography,
} from "@mui/material";
import {
  Visibility,
  VisibilityOff,
  LockOutlined,
} from "@mui/icons-material";
import { useNavigate, Link } from "react-router-dom";
import { signUp } from "../models/auth.model";
import * as Yup from "yup";
import { createTheme } from "@mui/material/styles";
import "./styles/signup.styles.scss"

const validationSchema = Yup.object().shape({
  first_name: Yup.string().required("First Name is required"),
  last_name: Yup.string().required("Last Name is required"),
  username: Yup.string().required("Invalid username").required("Username is required"),
  password: Yup.string().required("Password is required"),
});

export default function Signup(): JSX.Element {
  const [inputState, setInputState] = useState<signUp>({
    first_name: "",
    last_name: "",
    username: "",
    password: "",
  });

  const [isDisabled, setIsDisabled] = useState<boolean>(true);
  const [showPassword, setShowPassword] = useState<boolean>(false);
  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({});

  const { first_name, last_name, username, password } = inputState;
  const navigate = useNavigate();
  const defaultTheme = createTheme();

  const handleInput = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputState({
      ...inputState,
      [event.target.name]: event.target.value,
    });
  };

  useEffect(() => {
    validationSchema
      .validate(inputState, { abortEarly: false })
      .then(() => {
        setIsDisabled(false);
        setValidationErrors({});
      })
      .catch((err: { inner: any[]; }) => {
        const errors: Record<string, string> = {};
        err.inner.forEach((e) => {
          errors[e.path] = e.message;
        });
        setIsDisabled(true);
        setValidationErrors(errors);
      });
  }, [inputState]);

  const handleRegistration = () => {
    const { first_name, last_name, username, password } = inputState;
    const payload = {
      username: username,
      password: password,
      first_name: first_name,
      last_name: last_name,
    };
    registerUser(payload);
    console.log(payload);
  };

  const togglePasswordVisibility = () => {
    setShowPassword((prevShowPassword) => !prevShowPassword);
  };

  return (
    <ThemeProvider theme={defaultTheme}>
      <Container component="main" maxWidth="xs" className="signup-container">
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
                  name="first_name"
                  required
                  fullWidth
                  id="first_name"
                  label="First Name"
                  autoFocus
                  value={first_name}
                  onChange={handleInput}
                  error={!!validationErrors.first_name}
                  helperText={validationErrors.first_name}
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
                  value={last_name}
                  onChange={handleInput}
                  error={!!validationErrors.last_name}
                  helperText={validationErrors.last_name}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  id="username"
                  label="Username"
                  name="username"
                  autoComplete="username"
                  value={username}
                  onChange={handleInput}
                  error={!!validationErrors.username}
                  helperText={validationErrors.username}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  name="password"
                  label="Password"
                  type={showPassword ? "text" : "password"}
                  id="password"
                  autoComplete="new-password"
                  value={password}
                  onChange={handleInput}
                  error={!!validationErrors.password}
                  helperText={validationErrors.password}
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton onClick={togglePasswordVisibility} edge="end">
                          {showPassword ? <VisibilityOff /> : <Visibility />}
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
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
