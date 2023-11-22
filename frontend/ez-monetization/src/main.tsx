import * as React from "react";
import * as ReactDOM from "react-dom/client";

import "./index.css";

import App from "./App";
import { ToastContainer } from "react-toastify";


ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ToastContainer
      position="bottom-right"
      autoClose={2000}
      hideProgressBar={false}
      newestOnTop={false}
      closeOnClick
      rtl={false}
      pauseOnFocusLoss
      draggable
      pauseOnHover
    />
    <App />
  </React.StrictMode>
);