export interface AuthState {
  isAuthenticated: boolean;
  accessToken: string | null;
  refreshToken: string | null;
  userType: string | null;
  login: (accessToken: string, refreshToken: string) => void;
  logout: () => void;
}
export interface signUp {
  username: string;
  password: string;
  first_name: string;
  last_name: string;
}

export interface logIn {
  email: string;
  password: string;
}
