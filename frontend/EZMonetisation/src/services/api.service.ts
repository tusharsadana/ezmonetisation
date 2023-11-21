import axios from "axios";
import { toast } from "react-toastify";

export const axiosAPIConfig = {
    baseURL: import.meta.env.BASE_URL,
    timeout: 50000,
    headers: {
        "Content-Type": "application/json",
    },
};

export const logoutStatusCodes = [401, 403];

export const axiosAPI = axios.create(axiosAPIConfig);

axiosAPI.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

axiosAPI.interceptors.response.use((response) => {
    return response;
}, (error) => {
    console.log(error.response);
    toast.error(error.response.statusText);
    if (logoutStatusCodes.includes(error.response.status)) {
        localStorage.removeItem("token");
        window.location.href = "/login";
    }
    return Promise.reject(error);
});