import React from "react";
import "./vehicleinfo.css";

export const VoiInfo = ({ key, vehicles, visible }) => {

    return (
        <div className={"vehicle-info voi" + key}>
            <div className="vehicle-info-header">
                <h3>Available Vois:</h3>
                <div className="vehicles">
                    {vehicles.map((vehicle, key) => {
                        return <div key={key} className="vehicle">
                            <div className="vehicle-name"><b>{vehicle.reg}</b></div>
                            <div className="vehicle-battery">Battery: {vehicle.battery}%</div>
                        </div>
                    })}
                </div>
            </div> 
        </div>
    );
}