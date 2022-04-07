import {useRef, useState, useEffect} from "react";
import {Map, Marker, ScaleControl, Source, Layer} from 'react-map-gl';
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faMagnifyingGlass, faBus, faTrain, faChargingStation, faBicycle} from "@fortawesome/free-solid-svg-icons";
import transportData from "./sample.json";
import "./map.css";
import 'mapbox-gl/dist/mapbox-gl.css';

export const token = process.env.REACT_APP_MAPBOX_API_TOKEN;

export const Mapbox = ({searchBarVisibility, setSearchBarVisibility, lng, lat, centre, setCentre, route}) => {
    const API_URL = process.env.REACT_APP_BACKEND_URL;

    const [zoom, setZoom] = useState(15);
    const [height, setHeight] = useState(document.documentElement.clientHeight);
    const [width, setWidth] = useState(document.documentElement.clientWidth);
    const [dragStart, setDragStart] = useState([0, 0])
    const [transport, setTransport] = useState({});
    const [transportInterval, setTransportInterval] = useState(null);

    useEffect(() => {
        const handleResize = () => {
            const [newWidth, newHeight] = [document.documentElement.clientWidth, document.documentElement.clientHeight];
            setHeight(newHeight);
            setWidth(newWidth);
        }
        window.addEventListener("resize", handleResize);

        return () => window.removeEventListener("resize", handleResize);
    }, [height, width]);

    const getTransportInfo = () => {
        /*
        const params = {
                lat: centre[0],
                long: centre[1],
                radius: zoom * 10
            },
            url = new URL(API_URL + "transport");

        url.search = new URLSearchParams(params).toString();
        fetch(url)
            .then(resp => resp.json())
            .then(({data}) => {
                setTransport(data);
            })
        */
        setTransport(transportData.data);
    }

    useEffect(() => {
        getTransportInfo();
    }, [transport])


    const handleWheelZoom = ({originalEvent: {deltaY}}) => {
        setZoom(zoom - deltaY * (zoom / 10000));
    }

    const handleDrag = (e) => {
        if (centre.length > 0) {
            let scaleFactor = (5000 / Math.pow(zoom, 7));
            const newLat = centre[0] - ((dragStart[1] - e.originalEvent.screenY) * scaleFactor);
            const newLong = centre[1] + ((dragStart[0] - e.originalEvent.screenX) * scaleFactor);
            setCentre([newLat, newLong]);
            setDragStart([e.originalEvent.screenX, e.originalEvent.screenY]);
        }
    }

    const inObj = (obj, key) => Object.keys(obj).includes(key);

    const routeData = route !== null ? route.legs.map(l => l.path).flat(): [];

    const data = {
        type: "Feature",
        properties: {},
        geometry: {
            type: "LineString",
            coordinates: routeData
        }
    };

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
        <Marker longitude={lng} latitude={lat} color="red" onClick={() => false}/>
        {
            inObj(transport, "bus_stations") && transport["bus_stations"] && transport["bus_stations"].length > 0 &&
            transport["bus_stations"].map((bus, key) => {
                return <Marker key={key} longitude={bus.long} latitude={bus.lat} onClick={() => false}>
                    <FontAwesomeIcon icon={faBus} size={"lg"} />
                </Marker>
            })
        }
        {
            inObj(transport, "bus_stations") && transport["train_stations"]&& transport["train_stations"].length > 0 &&
            transport["train_stations"].map((train, key) => {
                return <Marker key={key} longitude={train.long} latitude={train.lat} onClick={() => false}>
                    <FontAwesomeIcon icon={faTrain} size={"lg"} />
                </Marker>
            })
        }
        {
            inObj(transport, "ev_chargers") && transport["ev_chargers"] && transport["ev_chargers"].length > 0 &&
            transport["ev_chargers"].map((train, key) => {
                return <Marker key={key} longitude={train.long} latitude={train.lat} onClick={() => false}>
                    <FontAwesomeIcon icon={faChargingStation} size={"lg"} />
                </Marker>
            })
        }
        {
            inObj(transport, "santander_cycles") && transport["santander_cycles"] && transport["santander_cycles"].length > 0 &&
            transport["santander_cycles"].map((train, key) => {
                return <Marker key={key} longitude={train.long} latitude={train.lat} onClick={() => false}>
                    <FontAwesomeIcon icon={faBicycle} size={"lg"} />
                </Marker>
            })
        }
        {
            inObj(transport, "vois") && transport["vois"] && transport["vois"].length > 0 &&
            transport["vois"].map((voi, key) => {
                return <Marker key={key} longitude={voi.long} latitude={voi.lat} onClick={() => false}>
                    <img src={"/voi-icon.svg"} width={15} height={15}/>
                    <span className={"icon-label"}>{voi.vehicles.length}</span>
                </Marker>
            })
        }
        {
            inObj(transport, "tiers") && transport["tiers"] && transport["tiers"].length > 0 &&
            transport["tiers"].map((voi, key) => {
                return <Marker key={key} longitude={voi.long} latitude={voi.lat} onClick={() => false}>
                    <img src={"/voi-icon.svg"} width={15} height={15}/>
                    <span className={"icon-label"}>{voi.vehicles.length}</span>
                </Marker>
            })
        }
        <Source id="polylineLayer" type="geojson" data={data}>
          <Layer
            id="lineLayer"
            type="line"
            source="my-data"
            layout={{
              "line-join": "round",
              "line-cap": "round"
            }}
            paint={{
              "line-color": "rgba(3, 170, 238, 0.5)",
              "line-width": 5
            }}
          />
        </Source>
        <div className={"map-controls"}>
            {/* TODO: make accessible */}
            <button onClick={() => setZoom(zoom + 1)}>+</button>
            <button onClick={() => setZoom(zoom - 1)}>-</button>
            <button onClick={() => setSearchBarVisibility(!searchBarVisibility)}><FontAwesomeIcon
                icon={faMagnifyingGlass}/></button>
        </div>
    </Map>;

}