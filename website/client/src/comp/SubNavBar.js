import React from 'react';
import { Link } from 'react-router-dom';
import './SubNavBar.css';

function SubNavBar() {
    return (
        <div className="subnavbar">
            <Link to="/famous-person" >Famous Person</Link>
            <Link to="/honored-one" >Honored One</Link>
        </div>
    );
}

export default SubNavBar;
