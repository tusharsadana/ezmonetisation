import './App.css'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from './pages/login';
import Home from './pages/home';
import Signup from './pages/signup';
import PrivateRoutes from './utils/private-route.utils';
import { AuthProvider } from './contexts/auth.context';
import PublicRoutes from './utils/public-route.utils';
import { ThemeProvider } from '@emotion/react';
import theme from './theme/ThemeProvider';
import { Grid } from '@mui/material';
import Dashboard from './pages/dashboard/dashboard';
import WatchHours from './pages/watch-hours';


function App() {

  return (
    <>
      <ThemeProvider theme={theme}>
        <Router>
          <AuthProvider>
            <Routes>
              {/* <Route element={<PrivateRoutes />}> */}
              <Route path="/" Component={Home} >
                <Route
                  path=""
                  element={<Dashboard />}
                />
                <Route
                  path="watch"
                  element={<WatchHours />}
                />
                <Route
                  path="sub"
                  element={<>
                    <Grid>

                      <Grid item xs={6} sm={6} md={6} lg={6} xl={6}>

                        <h1>Subscribers</h1>
                      </Grid>
                      <Grid item xs={6} sm={6} md={6} lg={6} xl={6}>

                        <h1>Subscribers</h1>
                      </Grid>

                    </Grid>

                  </>}
                />

              </Route>
              {/* </Route> */}
              {/* <Route element={<PublicRoutes />}> */}
              <Route path="/login" Component={Login} />
              <Route path="/signup" Component={Signup} />
              {/* </Route> */}

              {/* <Route path="/reset-password" Component={ResetPassword} /> */}
            </Routes>
          </AuthProvider>

        </Router>
      </ThemeProvider>
    </>
  )
}

export default App
