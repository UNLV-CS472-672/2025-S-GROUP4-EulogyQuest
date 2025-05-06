// File: website/client/src/App.js

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import NavBar from './comp/NavBar';
import Home from './comp/Home';
import Generatequest from './comp/Generatequest';
import About from './comp/about';
import FamousPerson from './comp/Famousperson';
import HonoredOne from './comp/Honoredone';
import QuestViewer from './QuestViewer';

function App() {
  return (
    <Router>
      <NavBar />
      
      {/* Main content area; add padding to avoid overlapping the fixed footer */}
      <main style={{ paddingBottom: '60px' }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/generate-quest" element={<Generatequest />} />
          <Route path="/about" element={<About />} />
          <Route path="/famous-person" element={<FamousPerson />} />
          <Route path="/honored-one" element={<HonoredOne />} />
          <Route path="/quests" element={<QuestViewer filename="last-quest.json" />} />
        </Routes>
      </main>

      {/* Fixed footer */}
      <footer
        style={{
          zIndex: 10,
          position: 'fixed',
          bottom: 0,
          width: '100vw',
          textAlign: 'center',
          padding: '1vh 0',
          background: 'linear-gradient(to bottom, #cfcfcf, #ffffff, #cfcfcf)',
          fontWeight: 300,
        }}
      >
        © 2025 Eulogy Quest™. All rights reserved.
      </footer>
    </Router>
  );
}

export default App;
