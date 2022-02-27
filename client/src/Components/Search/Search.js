import "./Search.css";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faXmark} from "@fortawesome/free-solid-svg-icons";
import {token} from "../Map/Mapbox";
import {useState} from "react";
import { Result } from "../SearchResult/Result";

export const Search = ({searchBarVisibility, setSearchBarVisibility, lat, lng, setCentre}) => {
    const [suggestions, setSuggestions] = useState([]);
    const [info, setInfo] = useState(undefined);
    const [hidden, setHidden] = useState(false);
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

    return (
        <div className={"modal"}>
            <div className="hide" style={{display: hidden ? "none": "block"}}>
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
                                setHidden(true);
                                fetch("https://909f-2001-630-e4-4220-55c7-d61c-6788-9101.ngrok.io/navigation/?src_long=-2.6027&src_lat=51.4545&dest_long=-2.6220&dest_lat=51.4637")
                                .then(res => res.json()).then(j => {setInfo(j.data);});
                            }}>{place.name}</div>)
                        }
                    </div>
                </form>
            </div>
            <div className="stuff">
                {info !== undefined && Result(info)}
            </div>
        </div>
    )
}