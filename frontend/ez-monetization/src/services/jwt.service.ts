// import { signIn, signOut } from "./auth.service";

// export const AUTH_PROVIDERS = {
//     USER_LIST: "user_list"
// }

// export const PERMISSIONS = {};

// const TOKEN_EXPIRATION_THRESHOLD = 60 * 1000;

// export const ACCESS_TOKEN_KEY = "ACCESS_TOKEN_KEY";
// export const REFRESH_TOKEN_KEY = "REFRESH_TOKEN_KEY";
// export const REFRESH_INTERVAL = 1000;

// class JWTService {
//     private static instance: JWTService;
//     public loggedIn: boolean = false;
//     public provider: string | null = null;
//     public role: string | null = null;
//     public permissions: string[] = [];
//     public email: string | null = null;
//     public initDefer: any = {
//         resolve: null,
//         reject: null,
//         promise: null
//     };

//     private token: string | null = null;
//     private refreshToken: string | null = null;
//     private refreshInterval: any = null;
//     private signOutMethod: any = null;
//     private location: string | null = null;

//     private constructor(runRefreshTokenInterval: boolean = true, provider: string = AUTH_PROVIDERS.USER_LIST) {
//         this.init(runRefreshTokenInterval, provider);
//     }

//     public init(runRefreshTokenInterval: boolean = true, provider: string = AUTH_PROVIDERS.USER_LIST) {
//         this.provider = provider;
//         this.location = window.location.href;
//         this.token = localStorage.getItem(ACCESS_TOKEN_KEY);
//         this.refreshToken = localStorage.getItem(REFRESH_TOKEN_KEY);
//         this.signOutMethod = signOut;
//         this.provider = provider;
//         const parsedToken = this.token ? JSON.parse(atob(this.token.split(".")[1])) : null;

//         // this.initDefer.promise = new Promise((resolve, reject) => {
//         //     this.initDefer.resolve = resolve;
//         //     this.initDefer.reject = reject;
//         // });

//         if (parsedToken) {
//             this.loggedIn = true;
//             this.role = parsedToken.role;
//             this.permissions = parsedToken.permissions;
//             this.email = parsedToken["email"];
//             if (runRefreshTokenInterval) {
//                 this.runRefreshTokenInterval();
//             }
//         }

//         if (this.token) {
//             if (!this.isTokenExpired(this.token) && !this.needToRefreshToken(this.token)) {
//                 this.loggedIn = true;
//                 this.runRefreshTokenInterval();
//                 // this.initDefer.resolve();
//                 // return this.initDefer.promise;
//             }

//             if (this.refreshToken && !this.isTokenExpired(this.refreshToken)) {
//                 this.refresh()
//                     .then(() => {
//                         // this.initDefer.resolve();
//                         // if (window.location.pathname === "/login") {
//                         //     window.location.href = "/";
//                         // }
//                     })
//                     .finally(() => {
//                         // this.initDefer.resolve();
//                         this.runRefreshTokenInterval();
//                     });
//                 // return this.initDefer.promise;
//             } else {
//                 // if (window.location.pathname !== "/login") {
//                 //     window.location.href = "/login";
//                 // }
//             }
//         } else {
//             // this.initDefer.reject();
//             // if (window.location.pathname !== "/login") {
//             //     window.location.href = "/login";
//             // }
//         }

//         if (runRefreshTokenInterval) {
//             this.runRefreshTokenInterval();
//         }
//         // return this.initDefer.promise;
//     }

//     public static getInstance(runRefreshTokenInterval: boolean, authProvider: string): JWTService {
//         if (!JWTService.instance) {
//             JWTService.instance = new JWTService(runRefreshTokenInterval, authProvider);
//         }
//         return JWTService.instance;
//     }

//     public setToken(token: string, refreshToken: string): void {
//         this.token = token;
//         this.refreshToken = refreshToken;
//         localStorage.setItem(ACCESS_TOKEN_KEY, token);
//         localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
//     }

//     public runRefreshTokenInterval() {
//         if (this.refreshInterval) {
//             clearInterval(this.refreshInterval);
//         }

//         this.refreshInterval = setInterval(() => {
//             if (
//                 this.token &&
//                 this.refreshToken &&
//                 !this.isTokenExpired(this.refreshToken) &&
//                 this.needToRefreshToken(this.token)
//             ) {
//                 this.refresh();
//             }
//         }, REFRESH_INTERVAL);
//     }

//     public getToken(): string | null {
//         return localStorage.getItem(ACCESS_TOKEN_KEY);
//     }

//     public isAuthenticated(): boolean {
//         return !!this.getToken();
//     }

//     public getRefreshToken(): string | null {
//         return this.refreshToken;
//     }

//     public async login(username: string, password: string) {

//         return signIn(username, password).then((response) => {
//             const decodedToken = this.decodeToken(response.access);
//             this.loggedIn = true;
//             this.role = decodedToken.role;
//             this.permissions = decodedToken.permissions;
//             this.setToken(response.access, response.refresh);
//         });
//     }

//     public setLoggedIn(loggedIn: boolean) {
//         this.loggedIn = loggedIn;
//     }

//     public refresh() {
//         const access = this.getToken();
//         const refreshToken = this.getRefreshToken();

//         // eslint-disable-next-line @typescript-eslint/ban-ts-comment
//         // @ts-ignore
//         return refresh({ access, refresh: refreshToken }).then((response) => {
//             const decodedToken = this.decodeToken(response.access);
//             this.loggedIn = true;
//             this.role = decodedToken.role;
//             // @ts-ignore
//             this.permissions = decodedToken.permissions;
//             this.setToken(response.access, response.refresh);
//         });
//     }

//     public logout() {
//         const access = this.getToken();
//         const refresh = this.getRefreshToken();
//         this.setToken("", "");
//         this.token = null;
//         this.refreshToken = null;
//         this.loggedIn = false;
//         this.role = null;
//         this.permissions = [];
//         this.email = null;

//         if (this.refreshInterval) {
//             clearInterval(this.refreshInterval);
//         }

//         if (access && refresh) {
//             this.signOutMethod({ access, refresh });
//         }
//     }

//     private decodeToken(token: string) {
//         const base64Url = token.split(".")[1];
//         const base64 = base64Url.replace("-", "+").replace("_", "/");
//         return JSON.parse(window.atob(base64));
//     }

//     public canHaveAccess(permissions: string[]) {
//         permissions.some((permission) => this.permissions.includes(permission));
//     }

//     public isTokenExpired(token: string) {
//         if (token) {
//             const decoded = this.decodeToken(token);
//             const exp = decoded.exp;
//             const date = new Date(0);
//             date.setUTCSeconds(exp);
//             return !(date.valueOf() > new Date().valueOf());
//         } else {
//             return true;
//         }
//     }

//     public needToRefreshToken(token: string) {
//         if (token) {
//             const decoded = this.decodeToken(token);
//             const date = new Date(0);
//             date.setUTCSeconds(decoded.exp);
//             const currentTime = new Date();
//             // @ts-ignore
//             const timeRemaining = date - currentTime;
//             const thirtyPercentTime = TOKEN_EXPIRATION_THRESHOLD * 0.3;

//             return timeRemaining <= thirtyPercentTime;
//         }
//     }

// }

// export const jwtService = JWTService.getInstance(true, AUTH_PROVIDERS.USER_LIST);
