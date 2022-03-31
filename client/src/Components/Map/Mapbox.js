import {useRef, useState, useEffect} from "react";
import ReactDOM from "react-dom";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faMagnifyingGlass, faBus, faTrain, faChargingStation, faBicycle} from "@fortawesome/free-solid-svg-icons";
import "./map.css";
import mapboxgl from '!mapbox-gl'; // eslint-disable-line import/no-webpack-loader-syntax
import 'mapbox-gl/dist/mapbox-gl.css';

mapboxgl.accessToken = process.env.REACT_APP_MAPBOX_API_TOKEN;

export const MapboxWindow = ({setSearchBarVisibility, searchBarVisibility, userLng, userLat, centre, setCentre}) => {
    const API_URL = process.env.REACT_APP_BACKEND_URL;
    const map = useRef(null);
    const mapContainer = useRef(null);

    const [lng, setLng] = useState(userLng);
    const [lat, setLat] = useState(userLat);
    const [zoom, setZoom] = useState(15);

    const [height, setHeight] = useState(document.documentElement.clientHeight);
    const [width, setWidth] = useState(document.documentElement.clientWidth);
    const [transport, setTransport] = useState({});

    const getTransportInfo = () => {
        console.log('getting transport')
        const params = {
                lat,
                long: lng,
                radius: zoom * 5
            },
            url = new URL(API_URL + "transport/");

        url.search = new URLSearchParams(params).toString();
        fetch(url)
            .then(resp => resp.json())
            .then(({data}) => {
                setTransport(data);
            })
    }

    useEffect(() => {
            const interval_length = 60000;
            const shouldFetch = (transport.timestamp === undefined) || (Date.now() - transport.timestamp) > interval_length;
            if (shouldFetch) {
                getTransportInfo();
            }

            const timeout_id = setTimeout(() => getTransportInfo(), interval_length);
            return () => clearTimeout(timeout_id);
        }
    );

    const inObj = (obj, key) => Object.keys(obj).includes(key);

    useEffect(() => {
        if (map.current) return; // initialize map only once
        map.current = new mapboxgl.Map({
            container: mapContainer.current,
            style: 'mapbox://styles/mapbox/dark-v10',
            center: [lng, lat],
            zoom,
        });
    });

    useEffect(() => {
        if (!map.current) return; // wait for map to initialize
        map.current.on('move', () => {
            setLng(map.current.getCenter().lng.toFixed(4));
            setLat(map.current.getCenter().lat.toFixed(4));
            setZoom(map.current.getZoom().toFixed(2));
        });
    });

    useEffect(() => {
        const markers = [];
        const clearMarkers = () => markers.forEach(marker => marker.remove())

        if (!map.current) return; // wait for map to initialize
        const userLocationMarker = document.createElement("div");
        userLocationMarker.classList.add('user-marker');
        markers.push(new mapboxgl.Marker(userLocationMarker).setLngLat([userLng, userLat]).addTo(map.current))

        if (transport === null) return clearMarkers;

        inObj(transport, "bus_stations") && transport["bus_stations"].length > 0 &&
        transport["bus_stations"].forEach(bus => {
            const elem = document.createElement('div');
            elem.classList.add('bus')
            ReactDOM.render(<FontAwesomeIcon icon={faBus} size={"2x"}/>, elem);
            markers.push(new mapboxgl.Marker(elem).setLngLat([bus.long, bus.lat]).addTo(map.current))
        })

        inObj(transport, "train_stations") && transport["train_stations"].length > 0 &&
        transport["train_stations"].forEach(train => {
            const elem = document.createElement('div');
            elem.classList.add('train')
            ReactDOM.render(<FontAwesomeIcon icon={faTrain} size={"2x"}/>, elem);
            markers.push(new mapboxgl.Marker(elem).setLngLat([train.long, train.lat]).addTo(map.current))
        })

        inObj(transport, "ev_chargers") && transport["ev_chargers"] && transport["ev_chargers"].length > 0 &&
        transport["ev_chargers"].forEach(ev => {
            const elem = document.createElement('div');
            elem.classList.add('ev_chargers')
            ReactDOM.render(<FontAwesomeIcon icon={faChargingStation} size={"2x"}/>, elem);
            markers.push(new mapboxgl.Marker(elem).setLngLat([ev.long, ev.lat]).addTo(map.current))
        })

        inObj(transport, "vois") && transport["vois"] && transport["vois"].length > 0 &&
        transport["vois"].forEach(bike => {
            const elem = document.createElement('div');
            elem.classList.add('santander_cycles')
            ReactDOM.render(<FontAwesomeIcon icon={faBicycle} size={"2x"}/>, elem);
            markers.push(new mapboxgl.Marker(elem).setLngLat([bike.long, bike.lat]).addTo(map.current))
        })

        console.log(transport)
        inObj(transport, "vois") && transport["vois"] !== null && transport["vois"].length > 0 &&
        transport["vois"].forEach(voi => {
            const elem = document.createElement('div');
            elem.classList.add('voi')
            ReactDOM.render(<>
                <img src={"/voi-icon.svg"} width={15} height={15} alt={'voi'}/>
                <span className={"icon-label"}>{voi.vehicles.length > 1 && voi.vehicles.length}</span>
            </>, elem);
            markers.push(new mapboxgl.Marker(elem).setLngLat([voi.long, voi.lat]).addTo(map.current))
        })
        inObj(transport, "tier") && transport["tier"] !== null && transport["tier"].length > 0 &&
        transport["tier"].forEach(voi => {
            const elem = document.createElement('div');
            elem.classList.add('voi')
            ReactDOM.render(<>
                <img src={"/voi-icon.svg"} width={15} height={15} alt={'voi'}/>
                <span className={"icon-label"}>{voi.vehicles.length > 1 && voi.vehicles.length}</span>
            </>, elem);
            markers.push(new mapboxgl.Marker(elem).setLngLat([voi.long, voi.lat]).addTo(map.current))
        })

        return clearMarkers;
    });

    return (
        <div>
            <div ref={mapContainer} className="map-container"/>
            <div className={"map-controls"}>
                {/* TODO: make accessible */}
                <button onClick={() => map.current.zoomTo(zoom+1)}>+</button>
                <button onClick={() => map.current.zoomTo(zoom-1)}>-</button>
                <button onClick={() => setSearchBarVisibility(!searchBarVisibility)}><FontAwesomeIcon
                    icon={faMagnifyingGlass}/></button>
            </div>

        </div>
    );


}

//
// return <Map
//     initialViewState={{
//         longitude: lat,
//         latitude: lng,
//         zoom
//     }}
//     scrollZoom={true}
//     doubleClickZoom={false}
//     mapboxAccessToken={token}
//     className={"map-container"}
//     style={{width, height}}
//     mapStyle="mapbox://styles/mapbox/dark-v10"
//     onWheel={handleWheelZoom}
//     onMove={handleDrag}
// >
//     <Marker longitude={lng} latitude={lat} color="red" onClick={() => false}/>
//     {
//         inObj(transport, "bus_stations") && transport["bus_stations"] && transport["bus_stations"].length > 0 &&
//         transport["bus_stations"].map((bus, key) => {
//             return <Marker key={key} longitude={bus.long} latitude={bus.lat} onClick={() => false}>
//                 <FontAwesomeIcon icon={faBus} size={"lg"}/>
//             </Marker>
//         })
//     }
//     {
//         inObj(transport, "bus_stations") && transport["train_stations"] && transport["train_stations"].length > 0 &&
//         transport["train_stations"].map((train, key) => {
//             return <Marker key={key} longitude={train.long} latitude={train.lat} onClick={() => false}>
//                 <FontAwesomeIcon icon={faTrain} size={"lg"}/>
//             </Marker>
//         })
//     }
//     {
//         inObj(transport, "ev_chargers") && transport["ev_chargers"] && transport["ev_chargers"].length > 0 &&
//         transport["ev_chargers"].map((train, key) => {
//             return <Marker key={key} longitude={train.long} latitude={train.lat} onClick={() => false}>
//                 <FontAwesomeIcon icon={faChargingStation} size={"lg"}/>
//             </Marker>
//         })
//     }
//     {
//         inObj(transport, "santander_cycles") && transport["santander_cycles"] && transport["santander_cycles"].length > 0 &&
//         transport["santander_cycles"].map((train, key) => {
//             return <Marker key={key} longitude={train.long} latitude={train.lat} onClick={() => false}>
//                 <FontAwesomeIcon icon={faBicycle} size={"lg"}/>
//             </Marker>
//         })
//     }
//     {
//         inObj(transport, "vois") && transport["vois"] && transport["vois"].length > 0 &&
//         transport["vois"].map((voi, key) => {
//             return <Marker key={key} longitude={voi.long} latitude={voi.lat} onClick={() => false}>
//                 <img src={"/voi-icon.svg"} width={15} height={15}/>
//                 <span className={"icon-label"}>{voi.vehicles.length}</span>
//             </Marker>
//         })
//     }
//     {
//         inObj(transport, "tiers") && transport["tiers"] && transport["tiers"].length > 0 &&
//         transport["tiers"].map((voi, key) => {
//             return <Marker key={key} longitude={voi.long} latitude={voi.lat} onClick={() => false}>
//                 <img src={"/voi-icon.svg"} width={15} height={15}/>
//                 <span className={"icon-label"}>{voi.vehicles.length}</span>
//             </Marker>
//         })
//     }
//     <div className={"map-controls"}>
//         {/* TODO: make accessible */}
//         <button onClick={() => setZoom(zoom + 1)}>+</button>
//         <button onClick={() => setZoom(zoom - 1)}>-</button>
//         <button onClick={() => setSearchBarVisibility(!searchBarVisibility)}><FontAwesomeIcon
//             icon={faMagnifyingGlass}/></button>
//     </div>
// </Map>;

/*
    useEffect(() => {
        const handleResize = () => {
            const [newWidth, newHeight] = [document.documentElement.clientWidth, document.documentElement.clientHeight];
            setHeight(newHeight);
            setWidth(newWidth);
        }
        window.addEventListener("resize", handleResize);

        return () => window.removeEventListener("resize", handleResize);
    }, [height, width]);

* */