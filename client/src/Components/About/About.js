import "./About.css"
import voi from "./voi.png"
import lime from "./lime.svg"
import santandercycles from "./santandercycles.png"
import transportapi from "./transportapi.png"
import openchargemap from "./openchargemap.png"

export const About = ({closeFunction}) => {
    return <div id="about">
            <div id="aboutBackground" onClick={closeFunction}></div>
            <div id="aboutContent">
                <h2>Welcome to GreenMap</h2>
                <p>
                    An environmentally friendly navigation platform allowing you to fully consider the environmental impact of your journeys. GreenMap aggregates data from a range of sustainable transport providers and calculates the carbon emissions of each journey, enabling you to make a more informed decision.
                </p>
                <p>Currently we support the following transport methods:</p>
                <img src={voi} alt="Voi Electric Scooters"/>
                <img src={lime} alt="Lime Electric Scooters"/>
                <img src={santandercycles} alt="Santander Cycels"/>
                <br/>
                <img src={transportapi} alt="Transport API" style={{height:"50dp", paddingBottom:"30dp"}}/>
                <img src={openchargemap} alt="Open Charge Map" style={{height:"80px", paddingBottom:"10px"}}/>
                <p>This project was developed by a group of students as part of <a href="https://cssbristol.co.uk/events/2022-02-26_boeing_hackathon/">The University of Bristol CSSxBoeing Hackathon 2022.</a> You can find the repository at <a href="https://github.com/mitchLui/greenmap">our GitHub</a></p>
                <p>To contact us:
                    <ul id="contacts">
                        <li>Mitch Lui: <a id="contact-link" href={"mailto:mitch@mitchlui.dev"}>mitch@mitchlui.dev</a></li>
                        <li>Matthew Swan: <a id="contact-link" href={"mailto:cv20549@bristol.ac.uk"}>cv20549@bristol.ac.uk</a></li>
                        <li>Artur Varosyan: <a id="contact-link" href={"mailto:artur.varosyan1@gmail.com"}>artur.varosyan1@gmail.com</a></li>
                        <li>Salman Khan: <a id="contact-link" href={"mailto:salman@msalmankhan.co.uk"}>salman@msalmankhan.co.uk</a></li>
                    </ul>
                </p>
            </div>
        </div>
}