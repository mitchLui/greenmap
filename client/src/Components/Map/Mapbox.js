import {useRef, useState, useEffect} from "react";
import {Map, Marker, ScaleControl} from 'react-map-gl';
import "./map.css";
import 'mapbox-gl/dist/mapbox-gl.css';

const token = "pk.eyJ1IjoibXNhbG1hbmtoYW4iLCJhIjoiY2wwNDg3aXJiMGIyYzNpb2czMWxkd2JzbyJ9.7fFFZSy33ckDNMdUlfUWGA";

export const Mapbox = () => {
    const [lng, setLng] = useState(0.0);
    const [lat, setLat] = useState(0.0);
    const [centre, setCentre] = useState([]);
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

    const handleWheelZoom = ({originalEvent: {deltaY}}) => {
        setZoom(zoom - deltaY*(zoom/10000));
    }

    const handleDrag = (e) => {
        if(centre.length > 0) {
            const scaleFactor = (5000/Math.pow(zoom, 7));
            console.log(scaleFactor)
            console.log(zoom)
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
        <Marker longitude={lng} latitude={lat} color="red" />
    </Map>;

}