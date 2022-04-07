import "./Search.css";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faXmark} from "@fortawesome/free-solid-svg-icons";
import {token} from "../Map/Mapbox";
import {useState} from "react";
import navigationData from './sample.json';

export const Search = ({searchBarVisibility, setSearchBarVisibility, lat, lng, setCentre, setInfo}) => {
    const [suggestions, setSuggestions] = useState([]);
    const geocode = (q) => {
        const params = {
            access_token: token,
            proximity: `${lat},${lng}`,
        }
        const url = new URL(`https://api.mapbox.com/geocoding/v5/mapbox.places/${q}.json`);
        url.search = new URLSearchParams(params).toString();
        fetch(url).then(resp => resp.json()).then(({features}) => {
            setSuggestions(features.map(feature => ({
                name: feature["place_name"],
                coords: feature["center"],
            })));
        })
    }

    return (
        <div className={"modal"}>
            <div>
                <button className={"close"} onClick={() => setSearchBarVisibility(!searchBarVisibility)}>
                    <FontAwesomeIcon icon={faXmark}/>
                </button>
                <form>
                    <label htmlFor={"search"}>Search</label>
                    <input type={"text"} id={"search"} placeholder={"Enter Search Term"}
                        onChange={({target: {value}}) => geocode(value)}/>
                    <div className={"suggestions"}>
                        {
                            suggestions.map((place, key) => <div key={key} className={"suggestion"} onClick={() => {
                                setSearchBarVisibility(false);
                                setCentre([51.4637, -2.6220]);
                                /*
                                const params = {
                                    src_long: Math.round(lng * 10000) / 10000,
                                    src_lat: Math.round(lat * 10000) / 10000,
                                    dest_long: Math.round(place.coords[0] * 10000) / 10000,
                                    dest_lat: Math.round(place.coords[1] * 10000) / 10000
                                }
                                const url = new URL(process.env.REACT_APP_BACKEND_URL + "navigation");
                                url.search = new URLSearchParams(params).toString();
                                fetch(url)
                                .then(res => res.json()).then(j => {setInfo(j.data);});
                                */
                               setInfo(navigationData.data);
                            }}>{place.name}</div>)
                        }
                    </div>
                </form>
            </div>
        </div>
    )
}