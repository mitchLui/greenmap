import "./Search.css";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faXmark} from "@fortawesome/free-solid-svg-icons";
import {token} from "../Map/Mapbox";

export const Search = ({searchBarVisibility, setSearchBarVisibility, lat, lng}) => {
    const geocode = (q) => {
        const params = {
            access_token: token,
            proximity: `${lng},${lng}`,
        }
        const url = new URL(`https://api.mapbox.com/geocoding/v5/mapbox.places/${q}.json`);
        url.search = new URLSearchParams(params).toString();
        fetch(url).then(resp => resp.json()).then(json => console.log(json))
    }

    return (
        <div className={"modal"}>
            <button className={"close"} onClick={() => setSearchBarVisibility(!searchBarVisibility)}>
                <FontAwesomeIcon icon={faXmark}/>
            </button>
            <form>
                <label htmlFor={"search"}>Search</label>
                <input type={"text"} id={"search"} placeholder={"Enter Search Term"}
                       onChange={({target: {value}}) => geocode(value)}/>
            </form>
        </div>
    )
}