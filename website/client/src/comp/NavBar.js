import React from "react";
import { Link } from "react-router-dom";
import "./NavBar.css";

// Navbar component
function NavBar() {
    return (
        <div className="navbar">
            <Link to="/about" >About</Link>
            <Link to="/prompt" class = "active">Prompt</Link>
        </div>
    );
}

export default NavBar;

