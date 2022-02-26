import {useRef, useState, useEffect} from "react";
import {Map, Marker} from 'react-map-gl';
import "./map.css";
import 'mapbox-gl/dist/mapbox-gl.css';

const token = "pk.eyJ1IjoibXNhbG1hbmtoYW4iLCJhIjoiY2wwNDg3aXJiMGIyYzNpb2czMWxkd2JzbyJ9.7fFFZSy33ckDNMdUlfUWGA";

export const Mapbox = () => {
    const [lng, setLng] = useState(0.0);
    const [lat, setLat] = useState(0.0);
    const [zoom, setZoom] = useState(9);
    const [height, setHeight] = useState(document.documentElement.clientHeight);
    const [width, setWidth] = useState(document.documentElement.clientWidth);

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

        console.log(lat, lng)
    }

    useEffect(() => {
        const id = navigator.geolocation.watchPosition(
            (pos) => {
                setCoords(pos.coords.latitude, pos.coords.longitude);
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


    return <Map
        initialViewState={{
            longitude: lng,
            latitude: lat,
            zoom: zoom
        }}
        mapboxAccessToken={token}
        className={"map-container"}
        style={{width, height}}
        mapStyle="mapbox://styles/mapbox/dark-v10"
    >
        <Marker longitude={lng} latitude={lat} color="red" />
    </Map>;

}