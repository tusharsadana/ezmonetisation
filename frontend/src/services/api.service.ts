import axios, { AxiosRequestConfig, AxiosResponse, AxiosError, AxiosRequestHeaders, InternalAxiosRequestConfig } from "axios";

class ApiError extends Error {
  constructor(message: string, public status?: number) {
    super(message);
    this.name = "ApiError";
  }
}

const api = axios.create({
  baseURL: import.meta.env.BASE_URL,
});

api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    config.headers = {
      ...config.headers,
      Accept: "application/json",
      "Content-Type": "application/json",
    } as AxiosRequestHeaders;
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response: AxiosResponse) => {
    return response.data;
  },
  (error: AxiosError) => {
    if (error.response) {
      throw new ApiError(
        `Request failed with status ${error.response.status}`,
        error.response.status
      );
    } else if (error.request) {
      throw new ApiError("No response received from the server");
    } else {
      throw new ApiError("Error setting up the request");
    }
  }
);

export const get = async <T>(url: string, config?: AxiosRequestConfig): Promise<T> => {
  const response = await api.get<T>(url, config);
  return response.data;
};

export const post = async <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
  const response = await api.post<T>(url, data, config);
  return response.data;
};

export const put = async <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
  const response = await api.put<T>(url, data, config);
  return response.data;
};

export const remove = async <T>(url: string, config?: AxiosRequestConfig): Promise<T> => {
  const response = await api.delete<T>(url, config);
  return response.data;
};
