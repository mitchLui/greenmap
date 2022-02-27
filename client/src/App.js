import logo from './logo.svg';
import './App.css';
import {Navbar} from "./Components/Navbar/Navbar";
import {Mapbox} from "./Components/Map/Mapbox";
import {Search} from "./Components/Search/Search";
import {useEffect, useState} from "react";

function App() {
    const [searchBarVisibility, setSearchBarVisibility] = useState(false)
    const [lat, setLat] = useState(0)
    const [lng, setLng] = useState(0)
    const [centre, setCentre] = useState([]);

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

            {
                searchBarVisibility &&
                <Search searchBarVisibility={searchBarVisibility} setSearchBarVisibility={setSearchBarVisibility}
                        lat={lat} lng={lng}/>
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
