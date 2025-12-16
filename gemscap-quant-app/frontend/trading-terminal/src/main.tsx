import React from "react";
import ReactDOM from "react-dom/client";
import Terminal from "./pages/Terminal";
import "./styles/global.css";

ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
).render(
  <React.StrictMode>
    <Terminal />
  </React.StrictMode>
);
