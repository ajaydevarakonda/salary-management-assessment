import { useState } from "react";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";

function decodeToken(token) {
  try {
    return JSON.parse(atob(token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/")));
  } catch {
    return {};
  }
}

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));

  const handleLogin = (newToken) => {
    localStorage.setItem("token", newToken);
    setToken(newToken);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  if (!token) return <Login onLogin={handleLogin} />;

  const { sub: username } = decodeToken(token);
  return <Dashboard token={token} username={username} onLogout={handleLogout} />;
}
