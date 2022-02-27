#* PRIVATE
from service import Service
from voi import VoiService
import requests
import json

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
            leg["from"] = part["from_point_name"]
            leg["to"] = part["from_point_name"]
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

    def get_routes_voi(self, from_lat: float, from_lon: float, to_lat: float, to_lon: float, voi_service: VoiService):
        routes = self.get_routes(from_lat, from_lon, to_lat, to_lon)
        if routes is None:
            return None
        newRoutes = []
        voi_service_cache = {}
        for route in routes["routes"][:1]:
            for part in route["route_parts"]:
                if part["mode"] == "foot":
                    f = (from_lat, from_lon)
                    t = (to_lat, to_lon)
                    if part["from_point_name"] != "Journey Origin":
                        f = (part["from_point"]["place"]["latitude"], part["from_point"]["place"]["longitude"])
                    if part["to_point_name"] != "Journey Destination":
                        t = (part["to_point"]["place"]["latitude"], part["to_point"]["place"]["longitude"])
                    print("Hi")
                    print(part)


if __name__ == "__main__":
    transport_service = PublicTransportRoutingService("TRANSPORTAPIAPPID", "TRANSPORTAPIAPPKEY")
    voi_service = VoiService("VOIAPIAUTHTOCKEN")
    res = transport_service.get_routes(51.449142, -2.581315, 51.504937, -2.562431)["routes"]
    with open("test_output.txt", "w") as file:
        file.write(json.dumps(res))
    #transport_service.get_routes_voi(51.449142, -2.581315, 51.504937, -2.562431, voi_service)
