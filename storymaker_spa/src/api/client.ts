/* Storymaker – typed fetch layer (Chunk C)

   – Thin wrapper over window.fetch with:
     • Automatic JSON marshaling / error bubbling
     • Generic <T> helpers
     • Run-time switch between real backend & in-memory mock (VITE_API_MOCK=true)
*/
import type {
  ApiResponse,
  Book,
  Character,
  LoginResponse,
  MeResponse,
} from './types';

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8777';
const USE_MOCK = import.meta.env.VITE_API_MOCK === 'true';

// -------------------- Real network --------------------
async function realFetch<T>(path: string, opts: RequestInit = {}): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(opts.headers || {}),
    },
    ...opts,
  });

  // Gracefully handle non-JSON responses
  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    // The Flask error handler uses { error, code } – surface that
    const msg = data?.error ?? res.statusText ?? 'Unknown error';
    throw new Error(msg);
  }
  return data as T;
}

// -------------------- Mock layer ----------------------
import mockFetch from './mock';
const baseFetch = USE_MOCK ? mockFetch : realFetch;

// -------------------- API helpers ---------------------
// Feel free to extend – component code stays type-safe.

// Books ------------------------------------------------
export const listBooks       = () => baseFetch<ApiResponse<Book[]>>('/api/books',   { headers: { Authorization: 'DEV' } });
export const createBook      = (payload: any) =>
  baseFetch<ApiResponse<{ book_id: string }>>('/api/books', {
    method: 'POST',
    body: JSON.stringify(payload),
    headers: { Authorization: 'DEV' },
  });

// Characters ------------------------------------------
export const listCharacters  = () => baseFetch<ApiResponse<Character[]>>('/api/characters', { headers: { Authorization: 'DEV' } });
export const createCharacter = (payload: any) =>
  baseFetch<ApiResponse<{ character_id: string }>>('/api/characters', {
    method: 'POST',
    body: JSON.stringify(payload),
    headers: { Authorization: 'DEV' },
  });

// Auth -------------------------------------------------
export const login           = (email: string, password = '') =>
  baseFetch<ApiResponse<LoginResponse>>('/api/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });

export const me              = (token: string) =>
  baseFetch<ApiResponse<MeResponse>>('/api/me', {
    headers: { Authorization: `Bearer ${token}` },
  });

// Export default for ad-hoc fetches
export default baseFetch;
