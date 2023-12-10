import { createContext, useContext, useState, useEffect } from "react";
import Cookies from "universal-cookie";
import React, { ReactNode } from "react";
import { IAuthState } from "../models/auth.model";
import path from "path";

const initialAuthState: IAuthState = {
    isAuthenticated: false,
    accessToken: null,
    refreshToken: null,
    userType: null,
    login: () => { },
    logout: () => { },
};

export const AuthContext = createContext<IAuthState>(initialAuthState);
export const ACCESS_TOKEN_KEY = "ACCESS_TOKEN_KEY";
export const REFRESH_TOKEN_KEY = "REFRESH_TOKEN_KEY";
export const USER_EMAIL = "USER_EMAIL";

export function AuthProvider({ children }: { children: ReactNode }): React.ReactElement {
    const cookies = new Cookies();
    const [accessToken, setAccessToken] = useState<string | null>(
        cookies.get(ACCESS_TOKEN_KEY)
    );
    const [refreshToken, setRefreshToken] = useState<string | null>(
        cookies.get(REFRESH_TOKEN_KEY)
    );
    const [userEmail, setUserEmail] = useState<string | null>(
        cookies.get(USER_EMAIL)
    );
    const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
    const [userType, setUserType] = useState<string | null>(null);

    useEffect(() => {
        if (accessToken && refreshToken) {
            setIsAuthenticated(true);
        }
    }, [accessToken, refreshToken]);

    useEffect(() => {
        const storedAccessToken = cookies.get(ACCESS_TOKEN_KEY);
        if (storedAccessToken) {
            setAccessToken(storedAccessToken);
        }
    }, []);

    function login(newAccessToken: string, newRefreshToken: string, userEmail: string) {
        cookies.set(ACCESS_TOKEN_KEY, newAccessToken, { path: "/" });
        cookies.set(REFRESH_TOKEN_KEY, newRefreshToken, { path: "/" });
        cookies.set(USER_EMAIL, userEmail, { path: "/" });
        setAccessToken(newAccessToken);
        setRefreshToken(newRefreshToken);
        setUserEmail(userEmail);
        setIsAuthenticated(true);
    }

    function logout() {
        cookies.remove(ACCESS_TOKEN_KEY, { path: "/" });
        cookies.remove(REFRESH_TOKEN_KEY, { path: "/" });
        cookies.remove(USER_EMAIL, { path: "/" });
        setAccessToken(null);
        setRefreshToken(null);
        setUserEmail(null);
        setIsAuthenticated(false);
    }

    return (
        <AuthContext.Provider
            value={{
                isAuthenticated,
                accessToken,
                refreshToken,
                userType,
                login,
                logout,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}