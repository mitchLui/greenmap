import React from "react";
import "./Navbar.css"

export const Navbar = () =>
    <header>
        <div className={"wrapper"}>
        <a href={"/"} className={"logo-link"}><Logo></Logo></a>
        <nav>
            <ul>
                <li><a href={"/"}>Home</a></li>
                <li><a href={"/"}>Help</a></li>
                <li><a href={"/"}>Contact</a></li>
            </ul>
        </nav>
        </div>
    </header>

export const Logo = () =>
    <h1 className={"logo"}><span className={"bold"}>Green</span>Map</h1>
