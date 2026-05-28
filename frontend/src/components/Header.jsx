function Profile({ username, onLogout }) {
  return (
    <div className="profile">
      <span className="profile-name">{username}</span>
      <div className="profile-menu">
        <div className="profile-menu-inner">
          <button onClick={onLogout}>Logout</button>
        </div>
      </div>
    </div>
  );
}

export default function Header({ username, view, onViewChange, onLogout }) {
  return (
    <header className="header">
      <span className="header-title">Salary Management</span>
      <nav className="nav">
        <button
          className={`nav-link${view === "insights" ? " active" : ""}`}
          onClick={() => onViewChange("insights")}
        >
          Insights
        </button>
        <button
          className={`nav-link${view === "employees" ? " active" : ""}`}
          onClick={() => onViewChange("employees")}
        >
          Employees
        </button>
      </nav>
      <Profile username={username} onLogout={onLogout} />
    </header>
  );
}
