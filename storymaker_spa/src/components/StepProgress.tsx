import React from 'react';

interface Props {
  current: number;      // 1-based
  total: number;
  labels: string[];
}

export default function StepProgress({ current, total, labels }: Props) {
  return (
    <ol style={{ display: 'flex', listStyle: 'none', padding: 0, marginBottom: '1rem' }}>
      {labels.map((label, idx) => {
        const step = idx + 1;
        const isActive = step === current;
        return (
          <li key={label} style={{
            flex: 1,
            textAlign: 'center',
            padding: '.3rem .5rem',
            borderBottom: `3px solid ${isActive ? 'dodgerblue' : '#ccc'}`,
            fontWeight: isActive ? 600 : 400
          }}>
            {step}. {label}
          </li>
        );
      })}
    </ol>
  );
}
