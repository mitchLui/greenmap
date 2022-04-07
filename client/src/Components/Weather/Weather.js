import "./Weather.css";
import {useEffect, useState} from "react";
import weatherData from "./sample.json";

export const Weather = ({lat, long}) => {
    const [weather, setWeather] = useState({time: null, data: null})

    useEffect(async () => {
            const hour = 60 * 60 * 1000;
            const shouldFetch = (weather.time === null) || (Date.now() - weather.time) > hour;
            if (shouldFetch) {
                const data = await getWeatherData(lat, long);
                setWeather({time: Date.now(), data})
            }
        }
    );

    if(!weather.time) return <></>;

    return (
        <div className={"weather"}>
            <div className="weather-info">
                <div className={"weather-icon"}>
                    <img src={weather.data.icon_url} alt={weather.data.description} />
                </div>
                <div className="weather-temp">
                    {weather.data.temp}&deg;C
                </div>
            </div>
        </div>
    )
};


const getWeatherData = (lat, long) => {
    /*
    const params = {
            lat,
            long,
        },
        url = new URL(process.env.REACT_APP_BACKEND_URL + "weather");

    url.search = new URLSearchParams(params).toString();
    return fetch(url).then(resp => resp.json()).then(({data}) => data).catch(e => console.error(e))
    */
   return weatherData.data;
}
