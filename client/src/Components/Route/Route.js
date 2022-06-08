const toRad = v => v * Math.PI / 180;
const toDeg = v => v * 180 / Math.PI;
export const middlePoint = (lat1, lng1, lat2, lng2) => {
    var dLng = toRad(lng2 - lng1);
    lat1 = toRad(lat1);
    lat2 = toRad(lat2);
    lng1 = toRad(lng1);
    var bX = Math.cos(lat2) * Math.cos(dLng);
    var bY = Math.cos(lat2) * Math.sin(dLng);
    var lat3 = Math.atan2(Math.sin(lat1) + Math.sin(lat2), Math.sqrt((Math.cos(lat1) + bX) * (Math.cos(lat1) + bX) + bY * bY));
    var lng3 = lng1 + Math.atan2(bY, Math.cos(lat1) + bX);
    return [toDeg(lng3), toDeg(lat3)];
}

export const Route = ({r, setCentre}) => {
    //console.log(r);
    // setCentre(r.start, r.end)
    // plot route on map
    // set zoom level (somehow)
    return <div>Showing Route</div>; // expand with more details
}