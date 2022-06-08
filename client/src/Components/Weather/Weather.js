import "./Weather.css";
import {useEffect, useState} from "react";
import weatherData from "./sample.json";

export const Weather = ({lat, long}) => {
    const [weather, setWeather] = useState({time: null, data: null})

    /*
    const [state, setState] = useState({});
setState(prevState => {
  return {...prevState, ...updatedValues};
});
    */

    useEffect(() => {
            const fetchWeather = () => {
                const hour = 60 * 60 * 1000;
                const shouldFetch = (weather.time === null) || (Date.now() - weather.time) > hour;
                if (shouldFetch) {
                    const data = getWeatherData(lat, long);
                    return data;
                } else {
                    return weather.data;
                }
            }
            setWeather(prevState =>{
                return {...prevState, data: fetchWeather()};
            })
        }
    , [lat, long, weather.time, weather.data]);

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
