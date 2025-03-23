import React from "react";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import NavBar from "./comp/NavBar";
import About from "./comp/about";
import Prompt from "./comp/prompt";

function App() {
    return (
        <Router>
            <NavBar />
            <Routes>
                <Route path="/prompt" element={<Prompt />} />
                <Route path="/about" element={<About />} />
            </Routes>
        </Router>
    );
}

export default App;