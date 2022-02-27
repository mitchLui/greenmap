import "./Result.css";

export const Result = (recommendations) => {
    return <div className="result">
        {recommendations.routes.routes.map(route => {
            return <div className="route">
                <div className="time-taken">
                    {route.time + "min time"}
                </div>
                <div className="emissions">
                    {route.emissions + "g of CO2 produced"}
                </div>
                    {(route.legs.map(leg => leg.mode))}
                <br />
            </div>
        })}
    </div>
}