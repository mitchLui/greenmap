import "./Weather.css";
import {useEffect, useState} from "react";

export const Weather = ({lat, long}) => {
    const [weather, setWeather] = useState(null)

    useEffect(async () => {
            const hour = 60 * 60 * 1000;
            if (!weather || (weather.time - Date.now()) > hour) {
                const data = await getWeatherData(lat, long);
                setWeather({time: Date.now(), data})
            }
        }
    );

    if(!weather) return <></>;

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
    const params = {
            lat,
            long,
        },
        url = new URL(process.env.REACT_APP_BACKEND_URL + "weather");

    url.search = new URLSearchParams(params).toString();
    return fetch(url).then(resp => resp.json()).then(({data}) => data)
}
