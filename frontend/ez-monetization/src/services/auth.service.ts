import { USER_EMAIL } from "../contexts/auth.context";
import { IAuthTokens, ISignUp, IUserDetails } from "../models/auth.model";
import { axiosAPI, axiosAPIConfig } from "./api.service";

export const signIn = (
  email: string,
  password: string
): Promise<IAuthTokens> => {
  return axiosAPI
    .post("/v1/auth/sign-in", { user_email: email, password })
    .then((response) => {
      return response.data;
    })
    .catch((error) => {
      return Promise.reject(error);
    });
};

export const signOut = async ({
  access,
  refresh,
}: IAuthTokens): Promise<any> => {
  return axiosAPI
    .post("/v1/auth/sign-out", { access, refresh })
    .then((response) => {
      return response.data;
    })
    .catch((error) => {
      return Promise.reject(error);
    });
};

export const signUp = async (userData: ISignUp): Promise<any> => {
  return axiosAPI
    .post("/v1/auth/sign-up", userData)
    .then((response) => {
      return response.data;
    })
    .catch((error) => {
      return Promise.reject(error);
    });
};

export const refresh = async ({
  access,
  refresh,
}: IAuthTokens): Promise<IAuthTokens> => {
  return axiosAPI
    .post("/v1/auth/refresh", { access, refresh })
    .then((response) => {
      return response.data;
    })
    .catch((error) => {
      return Promise.reject(error);
    });
};

export const getUserDetails = (email: string): Promise<IUserDetails> => {
  const urlWithParams = `/v1/auth/user_details?user_email=${email}`;
  return axiosAPI
    .get(urlWithParams, axiosAPIConfig)
    .then((response) => {
      return response.data;
    })
    .catch((error) => {
      return Promise.reject(error);
    });
};
