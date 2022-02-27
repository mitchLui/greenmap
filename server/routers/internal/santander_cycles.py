import requests
import xmltodict  # convert xml to json
import json
import haversine as hs  # used for distance calculations between coordinates

SANTANDER_URL = "https://tfl.gov.uk/tfl/syndication/feeds/cycle-hire/livecyclehireupdates.xml"
COST_PER_HALF_AN_HOUR = "2.00"


class SantanderCycles():

    def get_cycles(self, lat: float, lng: float, radius: float):
        r = requests.get(SANTANDER_URL)
        if r.status_code == 200:
            data = json.loads(json.dumps(xmltodict.parse(r.text)))
            stations = self.filter_by_distance(lat, lng, radius, data)
            stations = self.filter_information(stations)
            return stations
        else:
            return []

    def filter_by_distance(self, lat: float, lng: float, radius: float, data: dict):
        stations: list = []

        # Filter cycle stations by distance
        for station in data["stations"]["station"]:
            station_loc = (float(station["lat"]), float(station["long"]))
            dist: float = hs.haversine((lat, lng), station_loc, unit=hs.Unit.METERS)
            if dist <= radius:
                station["distance"] = dist
                stations.append(station)

        # Sort by closest cycle station
        stations = sorted(stations, key=lambda k: k["distance"])
        return stations

    def filter_information(self, stations: list[dict]):
        for station in stations:
            station.pop("id")
            station.pop("terminalName")
            station.pop("installed")
            station.pop("locked")
            station.pop("installDate")
            station.pop("removalDate")
            station.pop("temporary")
            station.pop("nbDocks")
            station["bikes"] = station.pop("nbBikes")
            station["spaces"] = station.pop("nbEmptyDocks")
            station["cost"] = COST_PER_HALF_AN_HOUR
        return stations


if __name__ == "__main__":
    cycle_service = SantanderCycles()
    print(cycle_service.get_cycles(51.5007, -0.1246, 1000))
