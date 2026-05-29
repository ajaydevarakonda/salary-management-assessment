export async function login(username, password) {
  const res = await fetch("/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  if (!res.ok) throw new Error("Invalid credentials");
  return res.json();
}

export async function listEmployees(token, { page = 1, pageSize = 20, search = "" } = {}) {
  const params = new URLSearchParams({ page, page_size: pageSize, search });
  const res = await fetch(`/api/employees?${params}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Failed to fetch employees");
  return res.json();
}

export async function createEmployee(body, token) {
  const res = await fetch("/api/employees", {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error("Failed to create employee");
  return res.json();
}

export async function updateEmployee(id, body, token) {
  const res = await fetch(`/api/employees/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error("Failed to update employee");
  return res.json();
}

export async function deleteEmployee(id, token) {
  const res = await fetch(`/api/employees/${id}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Failed to delete employee");
}

export async function getSalaryStats(country, token) {
  const res = await fetch(`/api/insights/salary-stats?country=${encodeURIComponent(country)}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Failed to fetch salary stats");
  return res.json();
}

export async function getSalaryByJobTitle(country, token) {
  const res = await fetch(`/api/insights/salary-by-job-title?country=${encodeURIComponent(country)}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Failed to fetch job title stats");
  return res.json();
}
