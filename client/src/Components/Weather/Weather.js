import "./Weather.css"

const weatherApiUrl = "http://localhost:80/weather";

export const Weather = ({lat, long}) => {
    
    const weatherApi = `${weatherApiUrl}?lat=${lat}&long=${long}`;

    const weatherData = fetch(weatherApi, {
        method: "GET",
        mode: "cors",
        headers: {
            "Allow-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        },
    }).then(res => res.json()).then(json => console.log(json));

    return (<div className={"weather"}>
                <div className={"weather-icon"}>
                    <img src={weatherData.data.icon_url} alt="weather icon"/>
                </div>
        </div>)
    
};