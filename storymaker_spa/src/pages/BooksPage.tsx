import React, { useEffect, useState } from 'react';
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
