import React from 'react';
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
