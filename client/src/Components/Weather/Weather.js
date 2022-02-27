import { useState } from "react";
import "./Weather.css"

const weatherApiUrl = "http://localhost:5001/weather";

export const WeatherBox = (lat, long) => {
    const [width, setWidth] = useState(200);
    const [height, setHeight] = useState(200);
    const [lat, setLat] = useState(0);
    const [long, setLong] = useState(0);

    useEffect(() => {
        navigator.geolocation.getCurrentPosition(function(position) {
            setLat(position.coords.latitude);
            setLong(position.coords.longitude);
    })});

    const weatherData = fetch(weatherApiUrl, {
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