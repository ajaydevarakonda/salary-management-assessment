import { useState } from "react";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";
import Employees from "./components/Employees";

function decodeToken(token) {
  try {
    return JSON.parse(atob(token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/")));
  } catch {
    return {};
  }
}

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [view, setView] = useState("insights");

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
  const shared = { token, username, view, onViewChange: setView, onLogout: handleLogout };

  return view === "employees"
    ? <Employees {...shared} />
    : <Dashboard {...shared} />;
}
