import { useState } from 'react'
import './App.css'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from './pages/login';
import Dashboard from './pages/dashboard';
import Signup from './pages/signup';

function App() {

  return (
    <>
      <Router>
        <Routes>
          <Route path="/" Component={Dashboard} />
          <Route path="/login" Component={Login} />
          <Route path="/signup" Component={Signup} />
          {/* <Route path="/reset-password" Component={ResetPassword} /> */}
        </Routes>
      </Router>
    </>
  )
}

export default App
