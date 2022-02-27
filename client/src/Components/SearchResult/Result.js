import "./Result.css";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBus, faP } from "@fortawesome/free-solid-svg-icons";
import { faPersonWalking } from "@fortawesome/free-solid-svg-icons";
import { faTrainSubway } from "@fortawesome/free-solid-svg-icons";


export const Result = (recommendations) => {
    return <div className="result">
        {recommendations.routes.routes.map(route => {
            return <div className="route">
                <div className="time-taken">
                    {Math.round(route.time) + "mins time - " + Math.round(route.dist) + "m"}
                </div>
                <div className="emissions">
                    {route.emissions + "g of CO2 produced"}
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