export async function login(username, password) {
  const res = await fetch("/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  if (!res.ok) throw new Error("Invalid credentials");
  return res.json();
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
