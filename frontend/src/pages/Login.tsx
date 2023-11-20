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
import { loginUser } from "../services/auth";
import { AuthContext } from "../contexts/authContext";
import * as Form from "@radix-ui/react-form";

import "../styles/styles.css";

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
    <Form.Root className="FormRoot">
      <Form.Field className="FormField" name="email">
        <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between' }}>
          <Form.Label className="FormLabel">Email</Form.Label>
          <Form.Message className="FormMessage" match="valueMissing">
            Please enter your email
          </Form.Message>
          <Form.Message className="FormMessage" match="typeMismatch">
            Please provide a valid email
          </Form.Message>
        </div>
        <Form.Control onChange={(e) => { setInputState({ ...inputState, email: e.target.value }), console.log(inputState) }} asChild>
          <input className="Input" type="email" required />
        </Form.Control>
      </Form.Field>
      <Form.Field className="FormField" name="question">
        <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between' }}>
          <Form.Label className="FormLabel">Question</Form.Label>
          <Form.Message className="FormMessage" match="valueMissing">
            Please enter a question
          </Form.Message>
        </div>
        <Form.Control asChild>
          <textarea className="Textarea" required />
        </Form.Control>
      </Form.Field>
      <Form.Submit asChild>
        <button className="Button" style={{ marginTop: 10 }}>
          Post question
        </button>
      </Form.Submit>
    </Form.Root>
  );
}
