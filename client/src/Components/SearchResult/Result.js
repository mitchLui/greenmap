import "./Result.css";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBus, faPersonWalking, faTrainSubway, faArrowRightLong } from "@fortawesome/free-solid-svg-icons";

const getRouteTime = (route) => {
    if ("arr_time" in route && "dep_time" in route) {
        return route.dep_time.slice(11,16) + " - " + route.arr_time.slice(11,16);
    }
    return "12:00 - 14:00";
}

export const Result = (recommendations) => {
    return <div className="result">
        {recommendations.routes.map((route, key) => {
            console.log(route);
            return <div className="route" key={key} onClick={() => {console.log(route)}}>
                <div className="route-time">
                    {getRouteTime(route)}
                </div>
                <div className="distance">
                    {Math.round(route.dist) + "m distance"}
                </div>
                <div className="emissions">
                    {route.emissions + "g of CO2 produced"}
                </div>
                {route.legs.map((leg, lk) => {
                    if (leg.mode === "bus") {
                        return <FontAwesomeIcon icon={faBus} key={lk} />
                    } else if (leg.mode === "walk") {
                        return <FontAwesomeIcon icon={faPersonWalking} key={lk} />
                    } else if (leg.mode === "train") {
                        return <FontAwesomeIcon icon={faTrainSubway} key={lk} />
                    } else if (leg.mode === "voi") {
                        return <img src="/voi-icon.svg" alt="voi" style={{width: "15px", height: "15px"}} key={lk} />
                    }
                    return <span key={lk}>{leg.mode}</span>;
                }).reduce((prev, curr) => [prev, <FontAwesomeIcon className="routeArrowIcon" icon={faArrowRightLong}/>, curr])}
                <span className="time-taken">
                    {Math.round(route.time) + "min time"}
                </span>
                <br />
            </div>
        })}
    </div>
}