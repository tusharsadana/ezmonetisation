import { Navigate, Outlet } from 'react-router-dom'
import { useContext } from "react";
import { AuthContext } from '../contexts/auth.context';


const PrivateRoutes = () => {
  const { isAuthenticated } = useContext(AuthContext);
  return (
    isAuthenticated ? <Outlet /> : <Navigate to='/login' />
  )
}

export default PrivateRoutes;