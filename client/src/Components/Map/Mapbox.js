import {useRef, useState, useEffect} from "react";
import {Map, Marker, ScaleControl} from 'react-map-gl';
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faMagnifyingGlass} from "@fortawesome/free-solid-svg-icons";
import "./map.css";
import 'mapbox-gl/dist/mapbox-gl.css';

export const token = "pk.eyJ1IjoibXNhbG1hbmtoYW4iLCJhIjoiY2wwNDg3aXJiMGIyYzNpb2czMWxkd2JzbyJ9.7fFFZSy33ckDNMdUlfUWGA";

export const Mapbox = ({searchBarVisibility, setSearchBarVisibility, lng, setLng, lat, setLat, centre, setCentre}) => {
    const [zoom, setZoom] = useState(15);
    const [height, setHeight] = useState(document.documentElement.clientHeight);
    const [width, setWidth] = useState(document.documentElement.clientWidth);
    const [dragStart, setDragStart] = useState([0, 0])

    useEffect(() => {
        const handleResize = () => {
            const [newWidth, newHeight] = [document.documentElement.clientWidth, document.documentElement.clientHeight];
            setHeight(newHeight);
            setWidth(newWidth);
        }
        window.addEventListener("resize", handleResize);

        return () => window.removeEventListener("resize", handleResize);
    }, [height, width]);

    const handleWheelZoom = ({originalEvent: {deltaY}}) => {
        setZoom(zoom - deltaY*(zoom/10000));
    }

    const handleDrag = (e) => {
        if(centre.length > 0) {
            let scaleFactor = (5000/Math.pow(zoom, 7));
            const newLat = centre[0] - ((dragStart[1] - e.originalEvent.screenY) * scaleFactor);
            const newLong = centre[1] + ((dragStart[0] - e.originalEvent.screenX) * scaleFactor);
            setCentre([newLat, newLong]);
            setDragStart([e.originalEvent.screenX, e.originalEvent.screenY]);
        }
    }


    return <Map
        scrollZoom={false}
        doubleClickZoom={false}
        zoom={zoom}
        latitude={centre[0] || 0}
        longitude={centre[1] || 0}
        mapboxAccessToken={token}
        className={"map-container"}
        style={{width, height}}
        mapStyle="mapbox://styles/mapbox/dark-v10"
        onWheel={handleWheelZoom}
        onDrag={handleDrag}
        onDragStart={({originalEvent: {screenX, screenY}}) => setDragStart([screenX, screenY])}
    >
        <Marker longitude={lng} latitude={lat} color="red"  onClick={() => false}/>
        <div className={"map-controls"}>
            {/* TODO: make accessible */}
            <button onClick={() => setZoom(zoom+1)}>+</button>
            <button onClick={() => setZoom(zoom-1)}>-</button>
            <button onClick={() => setSearchBarVisibility(!searchBarVisibility)}><FontAwesomeIcon icon={faMagnifyingGlass} /></button>
        </div>
    </Map>;

}