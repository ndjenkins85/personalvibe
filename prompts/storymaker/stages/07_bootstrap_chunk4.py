# Copyright © 2025 by Nick Jenkins. All rights reserved

# bootstrap_spa.py
# python prompts/storymaker/stages/07_bootstrap_chunk4.py
"""
Chunk 4 – Frontend SPA Skeleton
──────────────────────────────
Executing this script **once** will create/overwrite the minimal React/Vite
front-end needed to talk to the Storymaker Flask API.

• Generates the folder  <REPO>/storymaker_spa
• Wires Vite + React + React-Router (TypeScript)
• Adds helper API client using the local “DEV” auth shortcut
• Prints newbie-friendly “what next?” guide at the end
"""

from __future__ import annotations

import os
from pathlib import Path

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()


# ────────────────────────── helpers ──────────────────────────
def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def write(p: Path, text: str) -> None:
    """Idempotent writer – skip if unchanged."""
    if p.exists() and p.read_text() == text:
        return
    p.write_text(text)
    print(f"  • Wrote {p.relative_to(REPO)}")


# ────────────────────────── scaffold ─────────────────────────
SPA_DIR = REPO / "storymaker_spa"
SRC = SPA_DIR / "src"
PAGES = SRC / "pages"
COMP = SRC / "components"
ensure_dir(PAGES)
ensure_dir(COMP)

# -------------------------- package.json ---------------------
write(
    SPA_DIR / "package.json",
    """{
  "name": "storymaker-spa",
  "version": "0.0.1",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-router-dom": "^6.30.0"
  },
  "devDependencies": {
    "@types/react": "^18.3.1",
    "@types/react-dom": "^18.3.1",
    "@vitejs/plugin-react": "^4.4.1",
    "typescript": "^5.4.5",
    "vite": "^5.4.19"
  }
}
""",
)

# --------------------------- tsconfig ------------------------
write(
    SPA_DIR / "tsconfig.json",
    """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["DOM", "DOM.Iterable", "ES2020"],
    "module": "ESNext",
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "moduleResolution": "Node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": ["src"]
}
""",
)

# --------------------------- vite ----------------------------
write(
    SPA_DIR / "vite.config.ts",
    """import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: { port: 5173 },
});
""",
)

# -------------------------- index.html -----------------------
write(
    SPA_DIR / "index.html",
    """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Storymaker</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
</head>
<body>
  <div id="root"></div>
  <script type="module" src="/src/main.tsx"></script>
</body>
</html>
""",
)

# -------------------------- src/main.tsx ---------------------
write(
    SRC / "main.tsx",
    """import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
);
""",
)

# -------------------------- src/App.tsx ----------------------
write(
    SRC / "App.tsx",
    """import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import NavBar from './components/NavBar';
import IndexPage from './pages/IndexPage';
import BooksPage from './pages/BooksPage';
import CharactersPage from './pages/CharactersPage';
import StudioPage from './pages/StudioPage';
import AccountPage from './pages/AccountPage';

const App: React.FC = () => (
  <>
    <NavBar />
    <main style={{ padding: '1rem' }}>
      <Routes>
        <Route path="/" element={<IndexPage />} />
        <Route path="/books" element={<BooksPage />} />
        <Route path="/characters" element={<CharactersPage />} />
        <Route path="/studio" element={<StudioPage />} />
        <Route path="/account" element={<AccountPage />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </main>
  </>
);

export default App;
""",
)

# ---------------------- components/NavBar --------------------
write(
    COMP / "NavBar.tsx",
    """import React from 'react';
import { NavLink } from 'react-router-dom';

const base: React.CSSProperties = { marginRight: '1rem', textDecoration: 'none', color: '#444' };
const active: React.CSSProperties = { fontWeight: 'bold', color: 'dodgerblue' };

const link = (isActive: boolean): React.CSSProperties => ({ ...base, ...(isActive ? active : {}) });

export default function NavBar() {
  return (
    <nav style={{ padding: '1rem', borderBottom: '1px solid #ddd' }}>
      <NavLink to="/" end style={({ isActive }) => link(isActive)}>Home</NavLink>
      <NavLink to="/books" style={({ isActive }) => link(isActive)}>My Books</NavLink>
      <NavLink to="/characters" style={({ isActive }) => link(isActive)}>Characters</NavLink>
      <NavLink to="/studio" style={({ isActive }) => link(isActive)}>Studio</NavLink>
      <NavLink to="/account" style={({ isActive }) => link(isActive)}>Account</NavLink>
    </nav>
  );
}
""",
)

# ------------------------ api/client.ts ----------------------
write(
    SRC / "api" / "client.ts" if (SRC / "api").mkdir(exist_ok=True) else SRC / "api" / "client.ts",
    """const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8777';

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
""",
)

# --------------------------- pages ---------------------------
write(
    PAGES / "IndexPage.tsx",
    """import React from 'react';

export default function IndexPage() {
  return (
    <section>
      <h1>Create a custom kids book</h1>
      <p>🚧  Moving gallery coming soon.  For now, imagine beautiful book covers sliding by…</p>
    </section>
  );
}
""",
)

write(
    PAGES / "BooksPage.tsx",
    """import React, { useEffect, useState } from 'react';
import { listBooks } from '../api/client';

export default function BooksPage() {
  const [books, setBooks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listBooks()
      .then((r) => setBooks(r.data))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading…</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <section>
      <h1>My Books</h1>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem' }}>
        {books.map((b) => (
          <div key={b.id} style={{ width: '160px' }}>
            <div style={{
              width: '160px', height: '200px', background: '#eee',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              borderRadius: '4px', marginBottom: '.4rem',
            }}>
              {b.cover_image
                ? <img src={b.cover_image} alt={b.name} style={{ maxWidth: '100%', maxHeight: '100%' }} />
                : <span>Cover<br/>TBD</span>}
            </div>
            <strong style={{ fontSize: '.9rem' }}>{b.name}</strong><br/>
            <small>{new Date(b.created_at).toISOString().slice(0,10)}</small>
          </div>
        ))}
        <div style={{
          border: '2px dashed #aaa', width: '160px', height: '260px',
          display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '2rem',
        }}>+</div>
      </div>
    </section>
  );
}
""",
)

write(
    PAGES / "CharactersPage.tsx",
    """import React, { useEffect, useState } from 'react';
import { listCharacters } from '../api/client';

export default function CharactersPage() {
  const [chars, setChars] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    listCharacters().then((r) => { setChars(r.data); setLoading(false); });
  }, []);

  return (
    <section>
      <h1>Characters</h1>
      {loading ? <p>Loading…</p> : (
        <ul>
          {chars.map(c => <li key={c.id}>{c.name} ({c.type})</li>)}
        </ul>
      )}
      <p>🚧  Upload form & avatar tools coming in later chunks.</p>
    </section>
  );
}
""",
)

write(
    PAGES / "StudioPage.tsx",
    """import React from 'react';
export default function StudioPage() {
  return (
    <section>
      <h1>Story Studio</h1>
      <p>🚧  Two-step wizard (metadata ➜ script review) will be built in a future chunk.</p>
    </section>
  );
}
""",
)

write(
    PAGES / "AccountPage.tsx",
    """import React from 'react';
export default function AccountPage() {
  return (
    <section>
      <h1>My Account</h1>
      <p>🚧  Login & avatar selection UI coming soon.</p>
    </section>
  );
}
""",
)

# ------------------------- README ----------------------------
write(
    SPA_DIR / "README.md",
    """# Storymaker SPA

Bootstrapped by *Chunk 4*.

Run locally:

```bash
# 1. Ensure Node ≥ 20 is available (recommended via nvm)
nvm install 20 && nvm use 20

# 2. Install deps
cd storymaker_spa
npm install

# 3. Start dev server
npm run dev   # → http://localhost:5173
```

The dev server expects the Flask backend to be running on
`http://localhost:8777` (see `storymaker.api.app`).  During local
development the React app authenticates via the special
`Authorization: DEV` header defined in the Flask routes.
""",
)

# ────────────────────────── done ────────────────────────────
print(
    """
✅ Storymaker SPA skeleton generated.

What next?
──────────────────────────────────────────────────────────────
1.  Make sure **Node ≥ 20** is available – easiest via nvm:

        nvm install 20
        nvm use 20

2.  Install front-end dependencies:

        cd storymaker_spa
        npm install

3.  In **one** terminal start the Flask API:

        poetry run python -m storymaker.api.app

4.  In **another** terminal start the Vite dev server:

        npm run dev

    → open http://localhost:5173  (SPA)
    → API at http://localhost:8777

5.  Edit React/TS files under `storymaker_spa/src/` – hot-reload FTW.

Troubleshooting:
• If install fails, delete `node_modules` & `package-lock.json`, run `npm cache clean --force`, then `npm install`.
• The SPA talks to the API with the header `Authorization: DEV`, so no login flow is needed yet.
"""
)
