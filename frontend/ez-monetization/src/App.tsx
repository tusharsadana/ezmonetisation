import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/login";
import Home from "./pages/home";
import Signup from "./pages/signup";
import PrivateRoutes from "./utils/private-route.utils";
import { AuthProvider } from "./contexts/auth.context";
import { WatchHoursProvider } from "./contexts/watch-hours.context";
import PublicRoutes from "./utils/public-route.utils";
import { ThemeProvider } from "@emotion/react";
import theme from "./theme/ThemeProvider";
import { Grid } from "@mui/material";
import Dashboard from "./pages/dashboard/dashboard";
import WatchHours from "./pages/watch-hours";
import Plans from "./pages/plans";
import { loadStripe } from "@stripe/stripe-js";
import { Elements } from "@stripe/react-stripe-js";
import ReactGA from "react-ga4";
import React from "react";
import TransactionCancelledPage from "./pages/plans/plans.cancel";

const stripePromise = loadStripe(process.env.PK_TEST_KEY as string);

function App() {
  
    ReactGA.initialize("G-LVLTQWP613");
  
  ReactGA.send({ hitType: "pageview", page: "/login" });
  
  ReactGA.event({
    category: "User",
    action: "Logged In",
  });

  
  return (
    <>
      <ThemeProvider theme={theme}>
        <Router>
          <AuthProvider>
            <WatchHoursProvider>
              <Routes>
                <Route element={<PrivateRoutes />}>
                  <Route path="/" Component={Home}>
                    <Route path="" element={<Dashboard />} />
                    <Route
                      path="plans"
                      element={
                        <Elements stripe={stripePromise}>
                          <Plans />
                        </Elements>
                      }
                    />
                    <Route path="watch" element={<WatchHours />} />
                    <Route
                      path="sub"
                      element={
                        <>
                          <Grid>
                            <Grid item xs={6} sm={6} md={6} lg={6} xl={6}>
                              <h1>Subscribers</h1>
                            </Grid>
                            <Grid item xs={6} sm={6} md={6} lg={6} xl={6}>
                              <h3>Coming soon! Stay tuned</h3>
                            </Grid>
                          </Grid>
                        </>
                      }
                    />
                  </Route>
                  <Route path="plans/cancel" Component={TransactionCancelledPage} />
                </Route>
                <Route element={<PublicRoutes />}>
                  <Route path="/login" Component={Login} />
                  <Route path="/signup" Component={Signup} />
                </Route>

                {/* <Route path="/reset-password" Component={ResetPassword} /> */}
              </Routes>
            </WatchHoursProvider>
          </AuthProvider>
        </Router>
      </ThemeProvider>
    </>
  );
}

export default App;
