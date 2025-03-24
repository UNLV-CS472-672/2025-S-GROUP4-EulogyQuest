import React from "react";
import { Link } from "react-router-dom";
import "./NavBar.css";

// make nav bar look nice @Parham HAHAHA add a css file and include here please :D
function NavBar() {
    return (
        <div className="navbar">
            <Link to="/about" >About</Link>
            <Link to="/prompt" class = "active">Prompt</Link>
        </div>
    );
}

export default NavBar;

