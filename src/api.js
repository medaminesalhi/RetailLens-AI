export const API_BASE = (process.env.REACT_APP_API_URL || 'http://localhost:8000').replace(/\/+$/, '');

export function mediaUrl(path) {
  return `${API_BASE}${path}`;
}

export async function apiRequest(path, options) {
  const response = await fetch(`${API_BASE}/api/${path}`, options);
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.error || `Erreur HTTP ${response.status}`);
  }
  return data;
}
