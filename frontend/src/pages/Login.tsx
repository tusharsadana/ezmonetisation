import { useState, useEffect, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  Button,
  Grid,
  Paper,
  Stack,
  styled,
  TextField,
  Typography,
} from "@mui/material";
import { loginUser } from "../service/auth";
import { AuthContext } from "../contexts/authContext";

const Item = styled(Paper)(({ theme }) => ({
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: "center",
  borderRadius: theme.spacing(0),
  color: theme.palette.text.secondary,
}));

type loginState = {
  email: string;
  password: string;
};

export default function Login(): JSX.Element {
  const [inputState, setInputState] = useState<loginState>({
    email: "",
    password: "",
  });

  const { email, password } = inputState;
  const navigate = useNavigate();
  const { login } = useContext(AuthContext);

  const handleLogin = () => {
    loginUser(email, password)
      .then((res) => {
        login(res.accessToken, res.refreshToken);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  return (
    <Grid
      container
      spacing={0}
      direction="column"
      alignItems="center"
      justifyContent="center"
    >
      <Stack
        spacing={0}
        style={{ backgroundColor: "#ffffff95" }}
        sx={{ p: 2, width: "60vh" }}
      >
        <Item>
          <Typography
            variant="h4"
            gutterBottom
            component="div"
            align="center"
            mt={3}
          >
            Sign In
          </Typography>
        </Item>
        <Item>
          <TextField
            sx={{ width: "90%" }}
            label="Email"
            variant="outlined"
            size="small"
            defaultValue={email}
            onChange={(e) => {
              setInputState({ ...inputState, email: e.target.value });
            }}
          />
        </Item>
        <Item>
          <TextField
            sx={{ width: "90%" }}
            type="password"
            label="Password"
            variant="outlined"
            size="small"
            defaultValue={password}
            onChange={(e) => {
              setInputState({ ...inputState, password: e.target.value });
            }}
          />
        </Item>
        <Item>
          <Button variant="contained" color="secondary" onClick={handleLogin}>
            Login
          </Button>
        </Item>
        <Item></Item>
      </Stack>
    </Grid>
  );
}
