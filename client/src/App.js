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
                if(centre.length === 0) {
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
            <Mapbox searchBarVisibility={searchBarVisibility} setSearchBarVisibility={setSearchBarVisibility} lat={lat} setLat={setLat} lng={lng} setLng={lng} centre={centre} setCentre={setCentre}/>
            {
                searchBarVisibility &&
                <Search searchBarVisibility={searchBarVisibility} setSearchBarVisibility={setSearchBarVisibility} lat={lat} lng={lng} />
            }
        </div>
    );
}

export default App;
