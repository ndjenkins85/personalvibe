import React from 'react';
import { Character } from '../api/types';

interface Props {
  characters: Character[];
  value: string | null;
  onChange: (id: string) => void;
}

export default function CharacterSelect({ characters, value, onChange }: Props) {
  return (
    <select value={value ?? ''} onChange={(e) => onChange(e.target.value)} style={{ minWidth: '200px' }}>
      <option value="" disabled>Select…</option>
      {characters.map((c) => (
        <option key={c.id} value={c.id}>{c.name} ({c.type})</option>
      ))}
    </select>
  );
}
