import React, { useEffect, useState } from 'react';
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
