from .service import Service
from .clustering import oof_cluster
from typing import Dict
import haversine as hs  # used for distance calculations between coordinates
import requests
import json


VOIAPIUPDATEURL = "https://api.voiapp.io/v1/auth/session"
VOIAPIZONEURL = "https://api.voiapp.io/v1/zones"
VOIAPIVEHICLES = "https://api.voiapp.io/v2/rides/vehicles"

#TODO

def get_carbon_information(route: dict) -> Dict[str, int]:
    results = {}
    for part in route["route_parts"]:
        results[part["mode"]] = results.get(part["mode"], 0) + part["distance"]
    return results

class VoiService(Service):

    def update_api_key(self):
        success = False
        response = None
        while not success:
            body = f'{{"authenticationToken": "{self.app_id}"}}'
            r = requests.post(VOIAPIUPDATEURL, data=body)
            success = r.status_code == 200
            response = r.json()
        self.app_id = response["authenticationToken"]
        self.app_key = response["accessToken"]

    def __init__(self, api_app_keyname: str = None) -> None:
        super().__init__(api_app_keyname, "")
        # scheduler = BackgroundScheduler()
        # scheduler.add_job(self.update_api_key, 'interval', minutes=8)
        # scheduler.start()
        self.update_api_key()

    def get_vehicles(self, lat: float, long: float, radius: int):
        zone_id = self.get_zones(lat, long)
        if zone_id is None:
            return None
        zone_id = zone_id["zone_id"]
        r = requests.get(VOIAPIVEHICLES, {"zone_id": zone_id}, headers={"x-access-token": self.app_key})
        if r.status_code != 200:
            return None
        classes = r.json()["data"]["vehicle_groups"]
        if len(classes) == 0:
            return None
        vehicles = classes[0]["vehicles"]
        inRange = []
        for vehicle in vehicles:
            vLat = vehicle["location"]["lat"]
            vLong = vehicle["location"]["lng"]
            if hs.haversine((lat, long), (vLat, vLong), unit=hs.Unit.METERS) < radius:
                inRange.append({"reg": vehicle["short"], "battery": vehicle["battery"], "lat": vLat, "long": vLong})
        return oof_cluster(inRange)

    def get_zones(self, lat: float, lon: float) -> dict:
        r = requests.get(VOIAPIZONEURL, {"lat": lat, "lng": lon}, headers={"x-access-token": self.app_key})
        if r.status_code != 200:
            return None
        for zone in r.json()["zones"]:
            boundaries = zone["boundaries"]
            if boundaries["Lo"]["Lat"] <= lat <= boundaries["Hi"]["Lat"] and boundaries["Lo"]["Lng"] <= lon <= \
                    boundaries["Hi"]["Lng"]:
                return {"zone_id": zone["zone_id"], "start_cost": zone["start_cost"],
                        "minute_cost": zone["minute_cost"]}
        return None


if __name__ == "__main__":
    voi_service = VoiService("VOIAPIAUTHTOCKEN")
    print(json.dumps(voi_service.get_vehicles(51.461320, -2.599100, 500)))
