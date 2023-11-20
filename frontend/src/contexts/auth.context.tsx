import { createContext, useContext, useState, useEffect } from "react";
import Cookies from "universal-cookie";

type AuthState = {
  isAuthenticated: boolean;
  accessToken: string | null;
  refreshToken: string | null;
  userType: string | null;
  login : (accessToken: string, refreshToken: string) => void;
  logout : () => void;
};

const initialAuthState: AuthState = {
  isAuthenticated: false,
  accessToken: null,
  refreshToken: null,
  userType: null,
  login: () => {},
  logout: () => {},
};

export const AuthContext = createContext<AuthState>(initialAuthState);

import React, { ReactNode } from "react";

export function AuthProvider({ children }: { children: ReactNode }): React.ReactElement {
  const cookies = new Cookies();
  const [accessToken, setAccessToken] = useState<string | null>(
    cookies.get("access_tkn_lflw")
  );
  const [refreshToken, setRefreshToken] = useState<string | null>(
    cookies.get("refresh_tkn_lflw")
  );
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [userType, setUserType] = useState<string | null>(null);

  useEffect(() => {
    if (accessToken && refreshToken) {
      setIsAuthenticated(true);
    }
  }, [accessToken, refreshToken]);

  useEffect(() => {
    const storedAccessToken = cookies.get("access_tkn_lflw");
    if (storedAccessToken) {
      setAccessToken(storedAccessToken);
    }
  }, []);

  function login(newAccessToken: string, newRefreshToken: string) {
    cookies.set("access_tkn_lflw", newAccessToken, { path: "/" });
    cookies.set("refresh_tkn_lflw", newRefreshToken, { path: "/" });
    setAccessToken(newAccessToken);
    setRefreshToken(newRefreshToken);
    setIsAuthenticated(true);
  }

  function logout() {
    cookies.remove("access_tkn_lflw", { path: "/" });
    cookies.remove("refresh_tkn_lflw", { path: "/" });
    setAccessToken(null);
    setRefreshToken(null);
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
