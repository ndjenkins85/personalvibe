const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8777';

/**
 * Minimal fetch wrapper returning JSON and throwing on non-2xx.
 */
async function apiFetch<T>(path: string, opts: RequestInit = {}): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(opts.headers || {}) },
    ...opts,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error ?? res.statusText);
  return data as T;
}

export const listBooks = () => apiFetch<{ data: any[] }>('/api/books', { headers: { Authorization: 'DEV' } });
export const listCharacters = () => apiFetch<{ data: any[] }>('/api/characters', { headers: { Authorization: 'DEV' } });

export default apiFetch;
