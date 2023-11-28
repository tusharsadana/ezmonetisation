import { useState } from 'react'
import './App.css'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from './pages/login';
import Dashboard from './pages/dashboard';
import Signup from './pages/signup';
import PrivateRoutes from './utils/private-route.utils';
import { AuthProvider } from './contexts/auth.context';
import PublicRoutes from './utils/public-route.utils';
import { ThemeProvider } from '@emotion/react';
import theme from './theme/ThemeProvider';


function App() {

  return (
    <>
      <ThemeProvider theme={theme}>
        <Router>
          <AuthProvider>
            <Routes>
              <Route element={<PrivateRoutes />}>
                <Route path="/" Component={Dashboard} />
              </Route>
              <Route element={<PublicRoutes />}>
                <Route path="/login" Component={Login} />
                <Route path="/signup" Component={Signup} />
              </Route>

              {/* <Route path="/reset-password" Component={ResetPassword} /> */}
            </Routes>
          </AuthProvider>

        </Router>
      </ThemeProvider>
    </>
  )
}

export default App
