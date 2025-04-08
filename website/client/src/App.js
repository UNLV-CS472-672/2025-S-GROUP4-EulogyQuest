import React from "react";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

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
                <Route path="/generate-quest" element={<Generatequest />} />
                <Route path="/about" element={<About />} />
                <Route path="/famous-person" element={<FamousPerson />} />
                <Route path="/honored-one" element={<HonoredOne />} />
            </Routes>
        </Router>
    );
}

export default App;