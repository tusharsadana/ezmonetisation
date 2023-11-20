import axios, { AxiosResponse } from "axios";
import Cookies from "js-cookie";

const BASE_URL = "http://localhost:8000/api/"; // .env

const ROUTER_URL = "auth/"

const userAPI = axios.create({
  baseURL: BASE_URL,
});

export const registerUser = async (userData: any): Promise<void> => {
  try {
    let data = JSON.stringify(userData);
    await userAPI.post(`${ROUTER_URL}signup`, data, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    console.log("Success")
    window.location.replace("/login")
  } catch (error: any) {
    handleRequestError(error);
    throw error;
  }
};

export const loginUser = async (
  email: string,
  password: string
): Promise<{ accessToken: string; refreshToken: string }> => {
  try {
    const response: AxiosResponse<{
      accessToken: string;
      refreshToken: string;
    }> = await userAPI.post("/sign-in", { email, password });
    Cookies.set("accessToken", response.data.accessToken);
    Cookies.set("refreshToken", response.data.refreshToken);
    window.location.replace("/");
    return response.data;
  } catch (error: any) {
    handleRequestError(error);
    throw error;
  }
};

export const logoutUser = async (accessToken: string): Promise<void> => {
  try {
    await userAPI.post("/sign-out", null, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });
    Cookies.remove("accessToken");
    Cookies.remove("refreshToken");
    window.location.replace("/login");
  } catch (error: any) {
    handleRequestError(error);
    throw error;
  }
};

const handleRequestError = (error: any) => {
  if (error.response) {
    console.error("Request error:", error.response.status, error.response.data);
  } else if (error.request) {
    console.error("No response:", error.request);
  } else {
    console.error("Error:", error.message);
  }
};
