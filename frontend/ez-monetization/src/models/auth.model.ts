export interface IAuthTokens {
    access: string;
    refresh: string;
}

export interface IAuthState {
    isAuthenticated: boolean;
    accessToken: string | null;
    refreshToken: string | null;
    userType: string | null;
    login: (access: string, refresh: string, userEmail: string) => void;
    logout: () => void;
}
export interface ISignUp {
    username: string;
    password: string;
    first_name: string;
    last_name: string;
}

export interface ISignIn {
    email: string;
    password: string;
}

export interface IUserDetails {
    first_name: string, 
    last_name: string
}