import { React } from 'react';
import "./demo_banner.css";

export const DemoBanner = () => 
    <div className={"demo-container"}>
        This is a demo - the data is a sample and is not updated dynamically. This is because of the limits of our API keys.
        When searching for directions, the route is hardcoded to go from Park Street
        to Bristol Zoo. Changing the destination will not change the route.
    </div>