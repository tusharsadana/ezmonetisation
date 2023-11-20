import React, { FormEvent, useEffect, useState } from "react";
import { registerUser } from "../services/auth";
import { Button } from "@radix-ui/themes";
import * as Form from "@radix-ui/react-form";
import "../styles/styles.css";
import { useNavigate, Link } from "react-router-dom";

type signUp = {
  username: string;
  password: string;
  confirm_password: string;
  first_name: string;
  last_name: string;
};

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
  };

  return (
    <Form.Root
      onSubmit={(event: FormEvent<HTMLFormElement>) => {
        if (password === "") {
          event.preventDefault();
          return;
        }

        const data = Object.fromEntries(new FormData(event.currentTarget));
        event.preventDefault();
      }}
      className="h-full w-full"
    >
      <div className="flex h-full w-full flex-col items-center justify-center bg-muted">
        <div className="flex w-72 flex-col items-center justify-center gap-2">
          <span className="mb-6 text-2xl font-semibold text-primary">
            Sign up to ez-monetization
          </span>
          <div className="mb-3 w-full">
            <Form.Field name="username">
              <Form.Label className="data-[invalid]:label-invalid">
                Username <span className="font-medium text-destructive">*</span>
              </Form.Label>
              // TODO
              <Form.Control asChild>
                <Input
                  type="username"
                  onChange={({ target: { value } }) => {
                    handleInput({ target: { name: "username", value } });
                  }}
                  value={username}
                  className="w-full"
                  required
                  placeholder="Username"
                />
              </Form.Control>

              <Form.Message match="valueMissing" className="field-invalid">
                Please enter your username
              </Form.Message>
            </Form.Field>
          </div>
          <div className="mb-3 w-full">
            <Form.Field name="password" serverInvalid={password != confirm_password}>
              <Form.Label className="data-[invalid]:label-invalid">
                Password <span className="font-medium text-destructive">*</span>
              </Form.Label>
              // TODO
              <InputComponent
                onChange={(value) => {
                  handleInput({ target: { name: "password", value } });
                }}
                value={password}
                isForm
                password={true}
                required
                placeholder="Password"
                className="w-full"
              />

              <Form.Message className="field-invalid" match="valueMissing">
                Please enter a password
              </Form.Message>

              {password != confirm_password && (
                <Form.Message className="field-invalid">
                  Passwords do not match
                </Form.Message>
              )}
            </Form.Field>
          </div>
          <div className="w-full">
            <Form.Field
              name="confirmpassword"
              serverInvalid={password != confirm_password}
            >
              <Form.Label className="data-[invalid]:label-invalid">
                Confirm your password{" "}
                <span className="font-medium text-destructive">*</span>
              </Form.Label>

              <InputComponent
                onChange={(value) => {
                  handleInput({ target: { name: "cnfPassword", value } });
                }}
                value={confirm_password}
                isForm
                password={true}
                required
                placeholder="Confirm your password"
                className="w-full"
              />

              <Form.Message className="field-invalid" match="valueMissing">
                Please confirm your password
              </Form.Message>
            </Form.Field>
          </div>
          <div className="w-full">
            <Form.Submit asChild>
              <Button
                disabled={isDisabled}
                type="submit"
                className="mr-3 mt-6 w-full"
                onClick={() => {
                  handleRegistration();
                }}
              >
                Sign up
              </Button>
            </Form.Submit>
          </div>
          <div className="w-full">
            <Link to="/login">
              <Button className="w-full" variant="outline">
                Already have an account?&nbsp;<b>Sign in</b>
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </Form.Root>
  );
}
