import "./Search.css";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faXmark} from "@fortawesome/free-solid-svg-icons";
import {token} from "../Map/Mapbox";
import {useState} from "react";

export const Search = ({searchBarVisibility, setSearchBarVisibility, lat, lng, setCentre}) => {
    const [suggestions, setSuggestions] = useState([]);
    const geocode = (q) => {
        const params = {
            access_token: token,
            proximity: `${lng},${lng}`,
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

    console.log(suggestions)

    return (
        <div className={"modal"}>
            <button className={"close"} onClick={() => setSearchBarVisibility(!searchBarVisibility)}>
                <FontAwesomeIcon icon={faXmark}/>
            </button>
            <form>
                <label htmlFor={"search"}>Search</label>
                <input type={"text"} id={"search"} placeholder={"Enter Search Term"}
                       onChange={({target: {value}}) => geocode(value)}/>
                <div className={"suggestions"}>
                    {
                        suggestions.map((place, key) => <div className={"suggestion"} onClick={() => {
                            setCentre([place.coords[1], place.coords[0]]);
                            setSearchBarVisibility(false);
                        }}>{place.name}</div>)
                    }
                </div>
            </form>
        </div>
    )
}