#* PRIVATE
from .service import Service
import requests

PLACES_URL: str = "https://transportapi.com/v3/uk/public_journey.json"

def filter_results(res) -> list:
    journeys: list = []
    for route in res["routes"]:
        journey: dict = dict()
        duration = route["duration"].split(":")
        journey["time"] = float(duration[0]) * 60 + float(duration[1])
        journey["dist"] = route["distance"]
        journey["legs"] = []
        cumulative_dist = 0
        for part in route["route_parts"]:
            leg: dict = dict()
            leg["dist"] = part["distance"]
            leg["mode"] = "walk" if part["mode"] == "foot" else part["mode"]
            leg["path"] = part["coordinates"]
            leg["dep_time"] = part["departure_datetime"]
            leg["arr_time"] = part["arrival_datetime"]
            leg["src"] = part["from_point_name"]
            leg["dest"] = part["from_point_name"]
            leg["line"] = part["line_name"]
            journey["legs"].append(leg)
        journeys.append(journey)
    return journeys


class PublicTransportRoutingService(Service):

    # Find routes between two points inc walking, bus, train and ferry
    def get_routes(self, from_lat: float, from_lon: float, to_lat: float, to_lon: float):
        params = {"app_id": self.app_id, "app_key": self.app_key, "service": "silverrail",
                  "from": f"{from_lon}, {from_lat}", "to": f"{to_lon}, {to_lat}"}
        r = requests.get(PLACES_URL, params)
        if r.status_code == 200:
            return filter_results(r.json())
        else:
            return None


if __name__ == "__main__":
    transport_service = PublicTransportRoutingService("TRANSPORTAPIAPPID", "TRANSPORTAPIAPPKEY")
