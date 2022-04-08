import { React } from 'react';
import "./demo_banner.css";

export const DemoBanner = ({closeFunction}) => 
    <div className={"demo-container"} onClick={closeFunction}>
        <p>This is a demo - the data is static and is not updated dynamically. This is because of the limits of our API keys.
        When searching for directions, the route is hardcoded to go from Park Street
        to Bristol Zoo. Changing the destination will not change the route. </p>
        <p>If you would like to access a live version of the app for a demo, you can contact us through email. Our details are
            in the About section of the page, found above.</p>
        <p>Click this message to dismiss it.</p>
    </div>