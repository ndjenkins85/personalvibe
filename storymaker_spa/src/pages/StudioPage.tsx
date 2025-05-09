import React, { useEffect, useState } from 'react';
import { listCharacters, createBook } from '../api/client';
import { Character } from '../api/types';
import StepProgress from '../components/StepProgress';
import CharacterSelect from '../components/CharacterSelect';

// ------------------------- Step 1 form state --------------------------
interface BookForm {
  name: string;
  description: string;
  main_character: string | null;        // id
  side_characters: string[];            // ids
}

const emptyForm: BookForm = {
  name: '',
  description: '',
  main_character: null,
  side_characters: [],
};

export default function StudioPage() {
  // wizard state ------------------------------------------------------
  const [step, setStep] = useState<1 | 2>(1);

  // data --------------------------------------------------------------
  const [chars, setChars] = useState<Character[]>([]);
  const [loadingChars, setLoadingChars] = useState(true);

  // form --------------------------------------------------------------
  const [form, setForm] = useState<BookForm>(emptyForm);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [newBookId, setNewBookId] = useState<string | null>(null);

  // fetch characters once --------------------------------------------
  useEffect(() => {
    listCharacters()
      .then((r) => setChars(r.data))
      .catch((e) => setError(e.message))
      .finally(() => setLoadingChars(false));
  }, []);

  // utils -------------------------------------------------------------
  const update = <K extends keyof BookForm>(key: K, value: BookForm[K]) =>
    setForm((f) => ({ ...f, [key]: value }));

  const toggleSideCharacter = (id: string) =>
    update(
      'side_characters',
      form.side_characters.includes(id)
        ? form.side_characters.filter((c) => c !== id)
        : [...form.side_characters, id],
    );

  // -------------------------------------------------------------------
  // STEP 1 → submit
  // -------------------------------------------------------------------
  const next = async () => {
    setSaving(true);
    setError(null);
    try {
      const payload = {
        name: form.name,
        description: form.description,
        main_character: chars.find((c) => c.id === form.main_character),
        side_characters: chars.filter((c) => form.side_characters.includes(c.id)),
        chapters: [],
      };
      const res = await createBook(payload);
      setNewBookId(res.data.book_id);
      setStep(2);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setSaving(false);
    }
  };

  // -------------------------------------------------------------------
  // RENDER
  // -------------------------------------------------------------------
  return (
    <section style={{ maxWidth: '640px', margin: '0 auto' }}>
      <h1>Story Studio</h1>
      <StepProgress current={step} total={2} labels={['Story background', 'Review & finish']} />

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {step === 1 && (
        <>
          {loadingChars ? <p>Loading characters…</p> : (
            <form
              onSubmit={(e) => { e.preventDefault(); next(); }}
              style={{ display: 'flex', flexDirection: 'column', gap: '.8rem' }}
            >
              <label>
                Book name<br/>
                <input
                  type="text"
                  value={form.name}
                  onChange={(e) => update('name', e.target.value)}
                  required
                  maxLength={80}
                  style={{ width: '100%' }}
                />
              </label>

              <label>
                Description<br/>
                <textarea
                  value={form.description}
                  onChange={(e) => update('description', e.target.value)}
                  rows={3}
                  style={{ width: '100%' }}
                />
              </label>

              <label>
                Main character<br/>
                <CharacterSelect
                  characters={chars}
                  value={form.main_character}
                  onChange={(id) => update('main_character', id)}
                />
              </label>

              <fieldset style={{ border: '1px solid #ddd', padding: '.5rem' }}>
                <legend>Side characters (optional)</legend>
                {chars.map((c) => (
                  <label key={c.id} style={{ display: 'block' }}>
                    <input
                      type="checkbox"
                      checked={form.side_characters.includes(c.id)}
                      onChange={() => toggleSideCharacter(c.id)}
                      disabled={c.id === form.main_character}
                    />{" "}
                    {c.name} ({c.type})
                  </label>
                ))}
              </fieldset>

              <button type="submit" disabled={saving || !form.name || !form.main_character}>
                {saving ? 'Saving…' : 'Next'}
              </button>
            </form>
          )}
        </>
      )}

      {step === 2 && (
        <>
          <p>✅ Book stub created with id <code>{newBookId}</code>.</p>
          <p>Script generation & chapter editing UI will arrive in the next chunk.</p>
          <button onClick={() => { window.location.href = '/books'; }}>
            Go to “My Books”
          </button>
        </>
      )}
    </section>
  );
}
