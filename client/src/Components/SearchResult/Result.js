import "./Result.css";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBus, faP } from "@fortawesome/free-solid-svg-icons";
import { faPersonWalking } from "@fortawesome/free-solid-svg-icons";
import { faTrainSubway } from "@fortawesome/free-solid-svg-icons";

const formatTime = (time) => {
    time = Math.round(time)
    let hours = Math.floor(time / 60)
    let mins = time - (hours*60)
    if (hours < 1) {
        return mins + "mins time"
    } else {
        return hours + "h " + mins + "mins time"
    }
}

const formatDistance = (distance) => {
    distance = Math.round(distance)
    if (distance < 1000) {
        return distance + "m distance"
    } else {
        return (Math.round(distance / 10)/100) + "km distance"
    }
}

const formatEmission = (emissions) => {
    emissions = Math.round(emissions)
    if (emissions < 1000) {
        return emissions + "g of CO2 produced"
    } else {
        return (Math.round(emissions / 10)/100) + "kg of CO2 produced"
    }
    return emissions
}

export const Result = (recommendations) => {
    return <div className="result">
        {recommendations.routes.map(route => {
            return <div className="route">
                <div className="time-taken">
                    {formatTime(route.time)}
                </div>
                <div className="distance">
                    {formatDistance(route.dist)}
                </div>
                <div className="emissions">
                    {formatEmission(route.emissions)}
                </div>
                {route.legs.map(leg => {
                    if (leg.mode === "bus") {
                        return <FontAwesomeIcon icon={faBus} />
                    } else if (leg.mode === "walk") {
                        return <FontAwesomeIcon icon={faPersonWalking} />
                    } else if (leg.mode === "train") {
                        return <FontAwesomeIcon icon={faTrainSubway} />
                    } else if (leg.mode === "voi") {
                        return <img src="/voi-icon.svg" style={{width: "15px", height: "15px"}} />
                    }
                    return <span>{leg.mode}</span>;
                })}
                <br />
            </div>
        })}
    </div>
}