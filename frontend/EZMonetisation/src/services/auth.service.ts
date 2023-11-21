import { IAuthTokens } from "../models/auth.model"
import { axiosAPI } from "./api.service"


export const signIn = (email: string, password: string): Promise<IAuthTokens> => {
    return axiosAPI.post("/v1/auth/sign-in", { username: email, password }).then((response) => {
        return response.data;
    });
}

export const signOut = async ({ access, refresh }: IAuthTokens): Promise<any> => {
    return axiosAPI.post("/v1/auth/sign-out", { access, refresh }).then((response) => {
        localStorage.removeItem("token");
        localStorage.removeItem("refreshToken");
        return response.data;
    });

}

export const refresh = async ({ access, refresh }: IAuthTokens): Promise<IAuthTokens> => {
    return axiosAPI.post("/v1/auth/refresh", { access, refresh }).then((response) => {
        return response.data;
    });
}