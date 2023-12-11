import { IAuthTokens, ISignUp } from "../models/auth.model"
import { axiosAPI } from "./api.service"


export const signIn = (email: string, password: string): Promise<IAuthTokens> => {
    return axiosAPI.post("/v1/auth/sign-in", { user_email: email, password }).then((response) => {
        return response.data;
    }).catch((error) => {
        return Promise.reject(error);
    });
}

export const signOut = async ({ access, refresh }: IAuthTokens): Promise<any> => {
    return axiosAPI.post("/v1/auth/sign-out", { access, refresh }).then((response) => {
        return response.data;
    }).catch((error) => {
        return Promise.reject(error);
    });

}

export const signUp = async (userData: ISignUp): Promise<any> => {
    return axiosAPI.post("/v1/auth/sign-up", userData).then((response) => {
        return response.data;
    }).catch((error) => {
        return Promise.reject(error);
    });

}

export const refresh = async ({ access, refresh }: IAuthTokens): Promise<IAuthTokens> => {
    return axiosAPI.post("/v1/auth/refresh", { access, refresh }).then((response) => {
        return response.data;
    }).catch((error) => {
        return Promise.reject(error);
    });
}