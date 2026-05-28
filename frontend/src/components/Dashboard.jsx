import { useState, useEffect } from "react";
import Header from "./Header";
import { getSalaryStats, getSalaryByJobTitle } from "../api";

const COUNTRIES = [
  "Australia", "Brazil", "Canada", "France", "Germany",
  "India", "Netherlands", "Singapore", "United Kingdom", "United States",
];

const usd = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 });

function CountrySelect({ value, onChange }) {
  const [query, setQuery] = useState(value || "");
  const [open, setOpen] = useState(false);

  const filtered = COUNTRIES.filter((c) =>
    c.toLowerCase().includes(query.toLowerCase())
  );

  const select = (country) => {
    setQuery(country);
    setOpen(false);
    onChange(country);
  };

  return (
    <div className="combobox">
      <input
        value={query}
        onChange={(e) => { setQuery(e.target.value); setOpen(true); }}
        onFocus={() => setOpen(true)}
        onBlur={() => setTimeout(() => setOpen(false), 150)}
        placeholder="Select a country…"
      />
      {open && filtered.length > 0 && (
        <ul className="combobox-list">
          {filtered.map((c) => (
            <li key={c} onMouseDown={() => select(c)} className={c === value ? "selected" : ""}>
              {c}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function StatCard({ label, value }) {
  return (
    <div className="stat-card">
      <span className="stat-label">{label}</span>
      <span className="stat-value">{value}</span>
    </div>
  );
}

export default function Dashboard({ token, username, view, onViewChange, onLogout }) {
  const [country, setCountry] = useState("");
  const [stats, setStats] = useState(null);
  const [jobStats, setJobStats] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!country) return;
    setLoading(true);
    setError("");
    Promise.all([getSalaryStats(country, token), getSalaryByJobTitle(country, token)])
      .then(([s, j]) => {
        setStats(s[0] ?? null);
        setJobStats(j);
      })
      .catch(() => setError("Failed to load data for the selected country."))
      .finally(() => setLoading(false));
  }, [country, token]);

  return (
    <div className="page">
      <Header username={username} view={view} onViewChange={onViewChange} onLogout={onLogout} />

      <main className="main">
        <div className="toolbar">
          <label className="toolbar-label">Country</label>
          <CountrySelect value={country} onChange={setCountry} />
        </div>

        {error && <p className="error">{error}</p>}
        {loading && <p className="muted">Loading…</p>}

        {!loading && stats && (
          <>
            <div className="stats-grid">
              <StatCard label="Min Salary" value={usd.format(stats.minimum)} />
              <StatCard label="Max Salary" value={usd.format(stats.maximum)} />
              <StatCard label="Avg Salary" value={usd.format(stats.average)} />
              <StatCard label="Total Employees" value={stats.employee_count.toLocaleString()} />
            </div>

            {jobStats.length > 0 && (
              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Job Title</th>
                      <th>Avg Salary</th>
                      <th>Employees</th>
                    </tr>
                  </thead>
                  <tbody>
                    {jobStats.map((row) => (
                      <tr key={row.job_title}>
                        <td>{row.job_title}</td>
                        <td>{usd.format(row.average)}</td>
                        <td>{row.employee_count.toLocaleString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </>
        )}

        {!loading && !stats && country && !error && (
          <p className="muted">No data found for {country}.</p>
        )}

        {!country && (
          <p className="muted">Select a country to view salary insights.</p>
        )}
      </main>
    </div>
  );
}
