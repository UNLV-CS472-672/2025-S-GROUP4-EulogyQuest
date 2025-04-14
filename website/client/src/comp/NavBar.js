import React from "react";
import { Link } from "react-router-dom";
import "./NavBar.css";

// Navbar component
function NavBar() {
    return (
        <div className="navbar">
            <Link to="/" >Home</Link>
            <Link to="/generate-quest" class = "active">Generate quest</Link>
            <Link to="/about">About</Link>
        </div>
    );
}

export default NavBar;