import './App.css';
import {Navbar} from "./Components/Navbar/Navbar";
import {MapboxWindow as Mapbox} from "./Components/Map/Mapbox";
import {Search} from "./Components/Search/Search";
import {useEffect, useState} from "react";
import { Weather } from './Components/Weather/Weather';
import {Route} from "./Components/Route/Route";
import {LoaderWindow} from "./Components/Loader/Loader";


function App() {
    const [searchBarVisibility, setSearchBarVisibility] = useState(false)
    const [route, setRoute] = useState(null);
    const [lat, setLat] = useState(51.4558058);
    const [lng, setLng] = useState(-2.602799);
    const [centre, setCentre] = useState([51.4558058, -2.602799]);

    const setCoords = (lat, lng) => {
        setLng(lng);
        setLat(lat);
    }

    useEffect(() => {
        const id = navigator.geolocation.watchPosition(
            (pos) => {
                setCoords(pos.coords.latitude, pos.coords.longitude);
                if (centre.length === 0 || pos.coords.latitude !== centre[0] || pos.coords.latitude !== centre[1]) {
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

    const Wait_for_app_ready = () => {
        if ([centre, userLat, userLng].includes(null)) {
            return <LoaderWindow/>
        } else return (
            <>
                <Mapbox searchBarVisibility={searchBarVisibility} setSearchBarVisibility={setSearchBarVisibility}
                              userLat={lat} userLng={lng} centre={centre} setCentre={setCentre}/>
                <Clock/>
                <Weather lat={userLat} long={userLng}/>
                {
                    searchBarVisibility &&
                    <Search searchBarVisibility={searchBarVisibility} setSearchBarVisibility={setSearchBarVisibility}
                            lat={userLat} lng={userLng} setCentre={setCentre}/>
                }
                {route !== null && <Route route={route} setCentre={setCentre}/>}
            </>
        )
    }

    return (
        <div className="App">
            <Navbar/>
            <Wait_for_app_ready/>
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