import './App.css';
import {Navbar} from "./Components/Navbar/Navbar";
import {Mapbox} from "./Components/Map/Mapbox";
import {Search} from "./Components/Search/Search";
import {useEffect, useState} from "react";
import { Weather } from './Components/Weather/Weather';
import { Result } from "./Components/SearchResult/Result";
import { DemoBanner } from './Components/DemoBanner/DemoBanner';

const toRad = v => v * Math.PI / 180;
const toDeg = v => v * 180 / Math.PI;

const middlePoint = (lat1, lng1, lat2, lng2) => {
    var dLng = toRad(lng2 - lng1);
    lat1 = toRad(lat1);
    lat2 = toRad(lat2);
    lng1 = toRad(lng1);
    var bX = Math.cos(lat2) * Math.cos(dLng);
    var bY = Math.cos(lat2) * Math.sin(dLng);
    var lat3 = Math.atan2(Math.sin(lat1) + Math.sin(lat2), Math.sqrt((Math.cos(lat1) + bX) * (Math.cos(lat1) + bX) + bY * bY));
    var lng3 = lng1 + Math.atan2(bY, Math.cos(lat1) + bX);
    return [toDeg(lng3), toDeg(lat3)];
}


function App() {
    const [searchBarVisibility, setSearchBarVisibility] = useState(false);
    const [route, setRoute] = useState(null);
    const [info, setInfo] = useState(null);
    const [lat, setLat] = useState(51.4545);
    const [lng, setLng] = useState(-2.6027);
    const [dest, setDest] = useState([0, 0]);
    const [centre, setCentre] = useState([lat, lng]);
    const [showDemoWarning, setShowDemoWarning] = useState(true);

    const setCoords = (newLat, newLng) => {
        if (lat !== newLat || lng !== newLng) {
            setLng(lng);
            setLat(lat);
        }
    }

    useEffect(() => {
        if (route !== null) {
            const r = route;
            const start = r.legs[0].path[0];
            const end = r.legs[r.legs.length -1].path[r.legs[r.legs.length -1].path.length -1]
            setCentre(middlePoint(start[0], start[1], end[0], end[1]));
        }
    }, [route]);

    useEffect(() => {
        const id = navigator.geolocation.watchPosition(
            (pos) => {
                setCoords(pos.coords.latitude, pos.coords.longitude);
                // if (centre.length === 0 || pos.coords.latitude !== centre[0] || pos.coords.longitude !== centre[1]) {
                //     setCentre([pos.coords.latitude, pos.coords.longitude])
                // }
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

    /*
    removed from app return for now
    {
        route !== null && <Route r={route}/>
    }
    */

    return (
        <div className="App">
            <Navbar/>
            <Mapbox searchBarVisibility={searchBarVisibility} setSearchBarVisibility={setSearchBarVisibility} lat={lat}
                    setLat={setLat} lng={lng} setLng={lng} centre={centre} setCentre={setCentre} dest={dest} route={route}/>
            <Clock/>
            {showDemoWarning && <DemoBanner closeFunction={() => setShowDemoWarning(false)}/>}
            {<Weather lat={lat} long={lng} />}
            {
                searchBarVisibility &&
                <Search searchBarVisibility={searchBarVisibility} setSearchBarVisibility={setSearchBarVisibility}
                        lat={lat} lng={lng} setCentre={setCentre} setInfo={setInfo} setDest={setDest}/>
            }

            {
                info !== null && <Result recommendations={info} setSearchBarVisibility={setSearchBarVisibility} setRoute={setRoute}/>
            }
        </div>
    );
}

const Clock = () => {
    const [dateTime, setDateTime] = useState(new Date());

    useEffect(() => {
        if (dateTime){
            setInterval(()=> setDateTime(new Date()), 1000);
        }
    }, [dateTime]);
    

    return(
        <div className={"clock"}>
            <div className={"time"}>
                <span className={"big"}>
                    {dateTime.toLocaleTimeString('en-US', {
                        hour: 'numeric',
                        minute: 'numeric',
                        hour12: true,
                    })}
                </span>
            </div>
            <div className={"date"}>{                        
                dateTime.toLocaleDateString('en-GB', {
                    day: 'numeric',
                    month: 'short',
                    year: 'numeric',
                })}
            </div>
        </div>
    )
}
export default App;