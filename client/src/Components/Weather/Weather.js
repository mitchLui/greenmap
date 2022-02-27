import "./Weather.css";

export const Weather = (weather) => {
    return (<div className={"weather"}>
                {weather.icon_url !== undefined && <div className="weather-info">
                    <div className={"weather-icon"}>
                        <img src={weather.icon_url} alt="weather icon"/>
                    </div>
                    <div className="temperature">
                        {weather.temp}
                    </div>
                </div>}
        </div>)
};