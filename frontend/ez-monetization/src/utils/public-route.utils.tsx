import { Navigate, Outlet } from 'react-router-dom'
import { useContext } from "react";
import { AuthContext } from '../contexts/auth.context';


const PublicRoutes = () => {
    const { isAuthenticated } = useContext(AuthContext);
    return (
        isAuthenticated ? <Navigate to='/' /> : <Outlet />
    )
}

export default PublicRoutes;