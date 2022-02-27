import './App.css';
import {Navbar} from "./Components/Navbar/Navbar";
import {Mapbox} from "./Components/Map/Mapbox";
import {Search} from "./Components/Search/Search";
import {useEffect, useState} from "react";
import { Weather } from './Components/Weather/Weather';

const weatherApiUrl = "https://909f-2001-630-e4-4220-55c7-d61c-6788-9101.ngrok.io/weather";

function App() {
    const [searchBarVisibility, setSearchBarVisibility] = useState(false)
    const [weather, setWeather] = useState({icon_url: undefined});
    const [lat, setLat] = useState(51.4558058)
    const [lng, setLng] = useState(-2.602799)
    const [centre, setCentre] = useState([51.4558058, -2.602799]);
    const weatherApi = `${weatherApiUrl}?lat=${52}&long=${-2}`;

    fetch(weatherApi, {
        method: "GET",
        mode: "no-cors",
        headers: {
            "Allow-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        },
    }).then(res => res.json()).then(json => {setWeather(json.data)}).catch(err => {});

    const setCoords = (lat, lng) => {
        setLng(lng);
        setLat(lat);
    }

    useEffect(() => {
        const id = navigator.geolocation.watchPosition(
            (pos) => {
                setCoords(pos.coords.latitude, pos.coords.longitude);
                if (centre.length === 0) {
                    setCentre([pos.coords.latitude, pos.coords.longitude])
                }
            },
            (err) => {
                console.log(err);
            }, {
                enableHighAccuracy: true,
                timeout: 5000,
                maximumAge: 0
            }
        );


        return () => {
            navigator.geolocation.clearWatch(id);
        }
    })


    return (
        <div className="App">
            <Navbar/>
            <Mapbox searchBarVisibility={searchBarVisibility} setSearchBarVisibility={setSearchBarVisibility} lat={lat}
                    setLat={setLat} lng={lng} setLng={lng} centre={centre} setCentre={setCentre}/>
            <Clock />
            {Weather(weather)}
            {
                searchBarVisibility &&
                <Search searchBarVisibility={searchBarVisibility} setSearchBarVisibility={setSearchBarVisibility}
                        lat={lat} lng={lng} setCentre={setCentre}/>
            }
        </div>
    );
}

const Clock = () => {
    const [time, setTime] = useState("00:00");
    const [amPm, setAmPm] = useState("AM");
    const [date, setDate] = useState("27th February 2020");
    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "Decemmber"];
    useEffect(() => {
        const id = setTimeout(() => {
            const date = new Date(Date.now());
            let hour = date.getHours(),
                am = true,
                minute = date.getMinutes();

            if (hour > 12) {
                am = false;
                hour -= 12;
            }

            setTime(`${String(hour).padStart(2, 0)}:${String(minute).padStart(2, 0)}`);
            setAmPm(am ? "AM" : "PM");
            setDate(`${date.getDate()} ${months[date.getMonth()]} ${date.getFullYear()}`);
        }, 1000)
    })

    return(
        <div className={"clock"}>
            <div className={"time"}>
                <span className={"big"}>{time}</span> {amPm}
            </div>
            <div className={"date"}>{date}</div>
        </div>
    )

}

export default App;
