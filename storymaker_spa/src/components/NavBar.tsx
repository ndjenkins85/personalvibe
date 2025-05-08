import React from 'react';
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
