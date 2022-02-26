from .service import Service
import requests

PLACES_URL: str = "https://transportapi.com/v3/uk/places.json?"


class PublicTransportService(Service):

    def get_stations(self, lat: float, lng: float, transport_type: str):
        params: dict[str, str] = dict()
        params["app_id"] = self.app_id
        params["app_key"] = self.app_key
        params["lat"] = str(lat)
        params["lon"] = str(lng)
        params["type"] = "train_station" if transport_type == "train" else "bus_stop"
        r = requests.get(PLACES_URL, params)
        if r.status_code == 200:
            return self.filter_results(r.json())
        else:
            return None

    def get_train_stations(self, lat: float, lng: float):
        return self.get_stations(lat, lng, "train")

    def get_bus_stations(self, lat: float, lng: float):
        return self.get_stations(lat, lng, "bus_stop")

    def filter_results(self, results: dict):
        stations: list = []
        for entry in results["member"]:
            station: dict = dict()
            station["name"] = entry["name"]
            station["lat"] = entry["latitude"]
            station["lon"] = entry["longitude"]
            station["distance"] = entry["distance"]
            stations.append(station)
        return stations


if __name__ == "__main__":
    public_transport = PublicTransportService("TRANSPORTAPIAPPID", "TRANSPORTAPIAPPKEY")
    print(public_transport.get_stations(51.455795, -2.602835, "train"))
