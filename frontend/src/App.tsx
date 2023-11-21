import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
// import ResetPassword from "./pages/ResetPassword";
import "./App.css";


function App() {
  return (
    <>
      <Router>
        <Routes>
          <Route path="/" Component={Home} />
          <Route path="/signup" Component={Signup} />
          <Route path="/login" Component={Login} />
          {/* <Route path="/reset-password" Component={ResetPassword} /> */}
        </Routes>
      </Router>
    </>
  );
}

export default App;
