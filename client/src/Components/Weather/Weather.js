import { useState } from "react";
import "./Weather.css"

const weatherApiUrl = "http://localhost:5001/weather";

export const WeatherBox = (lat, long) => {
    const [width, setWidth] = useState(200);
    const [height, setHeight] = useState(200);

    const weatherData = await fetch(weatherApiUrl, {
        method: "POST",
        mode: "cors",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({"lat": lat, "long": long})
    }).then(res => res.json()).then(json => console.log(json));

    return <WeatherBox 
        width={width}
        height={height}
        weatherData={weatherData}
    />
    
};