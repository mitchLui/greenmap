#* PRIVATE
from service import Service
from voi import VoiService
import requests

PLACES_URL: str = "https://transportapi.com/v3/uk/public_journey.json"
MAXWALKRADIUS: int = 1000

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


if __name__ == "__main__":
    transport_service = PublicTransportRoutingService("TRANSPORTAPIAPPID", "TRANSPORTAPIAPPKEY")
