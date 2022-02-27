from .service import Service
from .clustering import g_cluster
import requests

TIER_URL: str = "https://platform.tier-services.io/v1/vehicle?"
TIER_PRICING_URL: str = "https://platform.tier-services.io/v2/pricing?"

#TODO

class TierScooterService(Service):

    def __init__(self, api_app_keyname: str = None, api_key_keyname: str = None) -> None:
        super().__init__(api_app_keyname, api_key_keyname)
        self.price_found = False
        self.start_price = ""
        self.per_min_cost = ""

    def get_scooters(self, lat: float, lng: float, radius: float):
        params: dict = {"lat": str(lat), "lng": str(lng), "radius": str(radius)}
        r = requests.get(TIER_URL, params=params, headers={"X-Api-Key": self.app_key})
        if r.status_code == 200:
            data = r.json()["data"]
            scooters = self.filter_data(data)
            scooter_groups = g_cluster(scooters)
            return scooter_groups
        else:
            return []

    def filter_data(self, data: list):
        scooters: list[dict] = []
        test = set()
        for entry in data:
            scooter: dict = dict()
            scooter["lat"] = entry["attributes"]["lat"]
            scooter["long"] = entry["attributes"]["lng"]
            scooter["reg"] = entry["attributes"]["licencePlate"]
            scooter["battery"] = entry["attributes"]["batteryLevel"]
            if not self.price_found:
                self.start_price, self.per_min_cost = self.get_cost(entry["id"])
                self.price_found = True
            scooter["start_price"], scooter["minute_cost"] = self.start_price, self.per_min_cost
            test.add((scooter["start_price"], scooter["minute_cost"]))
            scooters.append(scooter)

        return scooters

    def get_cost(self, scooter_id: str):
        params: dict = {"vehicleId": scooter_id}
        r = requests.get(TIER_PRICING_URL, params=params, headers={"X-Api-Key": self.app_key})
        if r.status_code == 200:
            data = r.json()["data"]["attributes"]
            start_price = data["rentalStartPrice"]
            per_minute_cost = data["rentalRunningPricePerMinute"]
            return start_price, per_minute_cost
        else:
            return None, None


if __name__ == "__main__":
    scooter_service = TierScooterService("", "TIERAPIKEY")
    scooters = scooter_service.get_scooters(51.5160, -0.1749, 1500)
    groups = g_cluster(scooters)
    print(groups)
