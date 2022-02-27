from service import Service
import requests

CYCLE_JOURNEY_URL: str = "https://transportapi.com/v3/uk/cycle/journey/"

"""
{ "distance": d,
  "path": [
    [ lon, lat ]
  ]
}
"""


class CycleRoutesService(Service):

    def get_route(self, src_lat: float, src_lng: float, dest_lat: float, dest_lng: float):
        params: dict[str, str] = dict()
        params["app_id"] = self.app_id
        params["app_key"] = self.app_key
        url = CYCLE_JOURNEY_URL + f"from/lonlat:{str(src_lng)},{str(src_lat)}/to/lonlat:{str(dest_lng)},{str(dest_lat)}"
        r = requests.get(url, params)
        if r.status_code == 200:
            print("200")
            print(r.json())
            results = r.json()
            return self.filter_results(results)
        else:
            return None

    def filter_results(self, results: dict):
        route: dict = dict()
        routes = results["routes"]
        if len(routes) >= 1:
            route["distance"] = routes[0]["distance"]
            route["path"] = [routes[0]["coordinates"], routes[0]["coordinates"]]
            return route
        else:
            return None


if __name__ == "__main__":
    cycle_route = CycleRoutesService("TRANSPORTAPIAPPID", "TRANSPORTAPIAPPKEY")
    print(cycle_route.get_route(51.529258, -0.134649, 51.506383, -0.088780))
