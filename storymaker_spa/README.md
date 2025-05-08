# Storymaker SPA

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
