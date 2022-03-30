import React from "react";
import "./Navbar.css"
import { About } from "../About/About.js"
import { useState } from "react";

export const Navbar = () => {
    const [showAbout, setShowAbout] = useState(false)
    return (<header>
        <div className={"wrapper"}>
        <a href={"/"} className={"logo-link"}><Logo></Logo></a>
        <nav>
            <ul>
                <li><a href={"/"}>Home</a></li>
                <li><a onClick={() => setShowAbout(true)}>About</a></li>
            </ul>
        </nav>
        </div>
        {showAbout && <About closeFunction={() => setShowAbout(false)}/>}
    </header>)
}
export const Logo = () =>
    <h1 className={"logo"}><span className={"bold"}>Green</span>Map</h1>
