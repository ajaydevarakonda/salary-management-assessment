import { useState, useEffect } from "react";
import Header from "./Header";
import { listEmployees, createEmployee, updateEmployee, deleteEmployee } from "../api";

const usd = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 });

const EMPTY = {
  first_name: "", last_name: "", job_title: "", department: "",
  country: "", email: "", salary: "", hire_date: "",
};

function EmployeeModal({ employee, onSave, onClose }) {
  const [form, setForm] = useState(employee || EMPTY);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const set = (key) => (e) => setForm((f) => ({ ...f, [key]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError("");
    try {
      await onSave(form);
    } catch {
      setError("Failed to save. Please check all fields.");
      setSaving(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <h2>{employee ? "Edit Employee" : "Add Employee"}</h2>
        {error && <p className="error">{error}</p>}
        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="field">
              <label>First Name</label>
              <input value={form.first_name} onChange={set("first_name")} required />
            </div>
            <div className="field">
              <label>Last Name</label>
              <input value={form.last_name} onChange={set("last_name")} required />
            </div>
            <div className="field">
              <label>Job Title</label>
              <input value={form.job_title} onChange={set("job_title")} required />
            </div>
            <div className="field">
              <label>Department</label>
              <input value={form.department} onChange={set("department")} required />
            </div>
            <div className="field">
              <label>Country</label>
              <input value={form.country} onChange={set("country")} required />
            </div>
            <div className="field">
              <label>Email</label>
              <input type="email" value={form.email} onChange={set("email")} required />
            </div>
            <div className="field">
              <label>Salary</label>
              <input type="number" value={form.salary} onChange={set("salary")} required min="0" step="0.01" />
            </div>
            <div className="field">
              <label>Hire Date</label>
              <input type="date" value={form.hire_date} onChange={set("hire_date")} required />
            </div>
          </div>
          <div className="form-actions">
            <button type="button" className="btn-secondary" onClick={onClose}>Cancel</button>
            <button type="submit" className="btn-primary" disabled={saving}>
              {saving ? "Saving…" : "Save"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default function Employees({ token, username, view, onViewChange, onLogout }) {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [editing, setEditing] = useState(null);

  const load = () => {
    setLoading(true);
    listEmployees(token)
      .then(setEmployees)
      .catch(() => setError("Failed to load employees."))
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, [token]);

  const filtered = employees.filter((e) => {
    const q = search.toLowerCase();
    return (
      e.first_name.toLowerCase().includes(q) ||
      e.last_name.toLowerCase().includes(q) ||
      e.email.toLowerCase().includes(q) ||
      e.country.toLowerCase().includes(q)
    );
  });

  const handleSave = async (form) => {
    if (editing.id) {
      await updateEmployee(editing.id, form, token);
    } else {
      await createEmployee(form, token);
    }
    setEditing(null);
    load();
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this employee?")) return;
    await deleteEmployee(id, token);
    setEmployees((prev) => prev.filter((e) => e.id !== id));
  };

  return (
    <div className="page">
      <Header username={username} view={view} onViewChange={onViewChange} onLogout={onLogout} />

      <main className="main">
        <div className="toolbar">
          <input
            className="search-input"
            placeholder="Search by name, email or country…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <button className="btn-primary" onClick={() => setEditing({})}>
            + Add Employee
          </button>
        </div>

        {error && <p className="error">{error}</p>}
        {loading && <p className="muted">Loading…</p>}

        {!loading && (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Job Title</th>
                  <th>Department</th>
                  <th>Country</th>
                  <th>Email</th>
                  <th>Salary</th>
                  <th>Hire Date</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((emp) => (
                  <tr key={emp.id}>
                    <td>{emp.first_name} {emp.last_name}</td>
                    <td>{emp.job_title}</td>
                    <td>{emp.department}</td>
                    <td>{emp.country}</td>
                    <td>{emp.email}</td>
                    <td>{usd.format(emp.salary)}</td>
                    <td>{emp.hire_date}</td>
                    <td className="actions">
                      <button className="btn-icon" onClick={() => setEditing(emp)}>Edit</button>
                      <button className="btn-icon danger" onClick={() => handleDelete(emp.id)}>Delete</button>
                    </td>
                  </tr>
                ))}
                {filtered.length === 0 && (
                  <tr>
                    <td colSpan="8" className="muted" style={{ textAlign: "center", padding: "24px" }}>
                      No employees found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </main>

      {editing !== null && (
        <EmployeeModal
          employee={editing.id ? editing : null}
          onSave={handleSave}
          onClose={() => setEditing(null)}
        />
      )}
    </div>
  );
}
