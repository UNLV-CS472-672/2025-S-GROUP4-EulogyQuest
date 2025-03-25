import React from "react";
import { Link } from "react-router-dom";

// make nav bar look nice @Parham HAHAHA add a css file and include here please :D
function NavBar() {
    return (
        <nav>
        <ul>
            <li>
            <Link to="/prompt">Prompt</Link>
            </li>
            <li>
            <Link to="/about">About</Link>
            </li>
        </ul>
        </nav>
    );
}

export default NavBar;