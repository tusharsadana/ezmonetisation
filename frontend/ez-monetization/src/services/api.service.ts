import axios, { AxiosError, AxiosRequestConfig, AxiosResponse, InternalAxiosRequestConfig } from "axios";
import { toast } from "react-toastify";
import Cookies from "universal-cookie";
import { ACCESS_TOKEN_KEY, REFRESH_TOKEN_KEY } from "../contexts/auth.context";

export const axiosAPIConfig = {
    baseURL: "http://localhost.com:8000/api",
    timeout: 50000,
    headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Credentials': true,

    },
};

export const logoutStatusCodes = [401, 403];

export const axiosAPI = axios.create(axiosAPIConfig);

axiosAPI.interceptors.request.use((config: InternalAxiosRequestConfig) => {
    // const token = new Cookies().get(ACCESS_TOKEN_KEY);
    // if (token) {
    //     config.headers.Authorization = `${token}`;
    // }
    return config;
}, (error: AxiosError) => {
    return Promise.reject(error);
});

axiosAPI.interceptors.response.use((response: AxiosResponse) => {
    return response;
}, async (error) => {
    toast.error(error.response?.statusText);
    const originalRequest = error.config;

    // If the error status is 401 and there is no originalRequest._retry flag,
    // it means the token has expired and we need to refresh it
    // if (error.response?.status === 401 && !originalRequest?._retry) {
    //     originalRequest._retry = true;

    //     try {
    //         const cookie = new Cookies();
    //         const refreshToken = cookie.get(REFRESH_TOKEN_KEY);
    //         const response = await axiosAPI.post('/v1/auth/refresh', { refresh: refreshToken });
    //         const { token } = response.data;

    //         cookie.set(ACCESS_TOKEN_KEY, token, { path: '/' });

    //         // Retry the original request with the new token
    //         originalRequest.headers.Authorization = `${token}`;
    //         return axios(originalRequest);
    //     } catch (error) {
    //         // Handle refresh token error or redirect to login
    //         toast.error("Internal server error");
    //     }
    // }
    toast.error(error.response?.statusText);
    return Promise.reject(error);
});

export const httpGet = async <T>(url: string, config?: AxiosRequestConfig): Promise<T> => {
    const response = await axiosAPI.get<T>(url, config);
    return response.data;
};

export const httpPost = async <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    const response = await axiosAPI.post<T>(url, data, config);
    return response.data;
};

export const httpPut = async <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    const response = await axiosAPI.put<T>(url, data, config);
    return response.data;
};

export const httpDelete = async <T>(url: string, config?: AxiosRequestConfig): Promise<T> => {
    const response = await axiosAPI.delete<T>(url, config);
    return response.data;
};