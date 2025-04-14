import React from "react";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import Home from "./comp/Home";
import NavBar from "./comp/NavBar";
import About from "./comp/about";
import Generatequest from "./comp/Generatequest";
import FamousPerson from "./comp/Famousperson";
import HonoredOne from "./comp/Honoredone";

function App() {
    return (
        <Router>
            <NavBar />
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/generate-quest" element={<Generatequest />} />
                <Route path="/about" element={<About />} />
                <Route path="/famous-person" element={<FamousPerson />} />
                <Route path="/honored-one" element={<HonoredOne />} />
            </Routes>
            <footer style={{
                zIndex: 10,
                position: "fixed",
                bottom: 0,
                width: "100vw",
                textAlign: "center",
                padding: "1vh 0",
                background: "linear-gradient(to bottom, #cfcfcf ,#ffffff, #cfcfcf)",
                fontWeight: "300",
                margintop: "10vh",
            }}>
                © 2025 Eulogy Quest™. All rights reserved.
            </footer>
        </Router>

    );
}

export default App;