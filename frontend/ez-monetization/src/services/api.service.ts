import axios, { AxiosError, AxiosRequestConfig, AxiosResponse, InternalAxiosRequestConfig } from "axios";
import { toast } from "react-toastify";
import Cookies from "universal-cookie";
import { ACCESS_TOKEN_KEY } from "../contexts/auth.context";

export const axiosAPIConfig = {
    baseURL: import.meta.env.BASE_URL,
    timeout: 50000,
    headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
    },
};

export const logoutStatusCodes = [401, 403];

export const axiosAPI = axios.create(axiosAPIConfig);

axiosAPI.interceptors.request.use((config: InternalAxiosRequestConfig) => {
    const token = new Cookies().get(ACCESS_TOKEN_KEY);
    if (token) {
        config.headers.Authorization = `${token}`;
    }
    return config;
}, (error: AxiosError) => {
    return Promise.reject(error);
});

axiosAPI.interceptors.response.use((response: AxiosResponse) => {
    return response;
}, (error: AxiosError) => {
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