import { React } from 'react';
import "./demo_banner.css";

export const DemoBanner = ({closeFunction}) => 
    <div className={"demo-container"} onClick={closeFunction}>
        This is a demo - the data is a sample and is not updated dynamically. This is because of the limits of our API keys.
        When searching for directions, the route is hardcoded to go from Park Street
        to Bristol Zoo. Changing the destination will not change the route. Click this message to dismiss it.
    </div>