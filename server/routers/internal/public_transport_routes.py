from service import Service
from voi import VoiService
import requests

PLACES_URL: str = "https://transportapi.com/v3/uk/public_journey.json"

def filter_results(routes):
    return routes

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
        pass


if __name__ == "__main__":
    transport_service = PublicTransportRoutingService("TRANSPORTAPIAPPID", "TRANSPORTAPIAPPKEY")
    # for part in transport_service.get_routes(51.449142, -2.581315, 51.504937, -2.562431)["routes"][0]["route_parts"]:
    #     for p in part[""]
