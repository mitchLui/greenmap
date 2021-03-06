from concurrent.futures import ThreadPoolExecutor, wait
import datetime
from traceback import format_exc
from typing import List
import haversine as hs
import json
import pytz

from .cycle_routes import CycleRoutesService
from .santander_cycles import SantanderCycles
from .tier_scooters import TierScooterService
from .voi import VoiService
from .cycle_routes import CycleRoutesService
from .timing_service import TimingService
from .carbon_offset import CarbonOffsetCalculator
from .public_transport_routes import PublicTransportRoutingService

# The acceptable distance to walk to the nearest vehicle
DISTANCE_TO_VEHICLE_LIMIT = 250  # metres

# The acceptable extra distance to the journey to get the vehicle
EXTRA_DISTANCE_TO_GET_VEHICLE = 10  # percentage

class RecommendedRoutesService:
    def __init__(self):
        self.cycle_routes_service = CycleRoutesService("TRANSPORTAPIAPPID", "TRANSPORTAPIAPPKEY")
        self.timing_service = TimingService()
        self.carbon_service = CarbonOffsetCalculator()
        self.public_transport = PublicTransportRoutingService("TRANSPORTAPIAPPID", "TRANSPORTAPIAPPKEY")

    # Given current coordinates and destination coordinates returns a list of routes with emission and time scores
    def get_recommend_routes(self, src_lat: float, src_lng: float, dest_lat: float, dest_lng: float):
        recommendations = {"routes": []}
        futures = []
        with ThreadPoolExecutor(max_workers=2) as e:
            futures.append(e.submit(self.find_cycling_vehicles, src_lat, src_lng, dest_lat, dest_lng))
            futures.append(e.submit(self.find_public_transport, src_lat, src_lng, dest_lat, dest_lng))
        recommendations["routes"].extend(futures[0].result()) 
        recommendations["routes"].extend(futures[1].result())
        return recommendations

    # Find journeys using Cycles, Vois and Tiers
    def find_cycling_vehicles(self, src_lat: float, src_lng: float, dest_lat: float, dest_lng: float) -> list:
        # Haversine distance from src to dest
        dist: float = hs.haversine((src_lat, src_lng), (dest_lat, dest_lng), unit=hs.Unit.METERS)

        routes = []

        # Initiate Service Objects
        cycle_service = SantanderCycles()
        tier_service = TierScooterService("", "TIERAPIKEY")
        voi_service = VoiService("VOIAPIAUTHTOCKEN")

        # Get Santander Cycles
        src_cycles = cycle_service.get_cycles(src_lat, src_lng, DISTANCE_TO_VEHICLE_LIMIT)
        src_cycle = self.closest_location(src_lat, src_lng, src_cycles)
        dest_cycles = cycle_service.get_cycles(dest_lat, dest_lng, DISTANCE_TO_VEHICLE_LIMIT)
        dest_cycle = self.closest_location(dest_lat, dest_lng, dest_cycles)
        if src_cycle is not None and dest_cycle is not None:
            res = self.filter_by_dist(src_lat, src_lng, dest_lat, dest_lng, src_cycle, dest_cycle, "cycle", dist)
            if len(res) > 0:
                self.get_cost(res["legs"], float(res["time"]))
                routes.append(res)

        # Get TIER Scooters
        src_tiers = tier_service.get_scooters(src_lat, src_lng, DISTANCE_TO_VEHICLE_LIMIT)
        src_tier = self.closest_location(src_lat, src_lng, src_tiers)
        dest_tiers = tier_service.get_scooters(dest_lat, dest_lng, DISTANCE_TO_VEHICLE_LIMIT)
        dest_tier = self.closest_location(dest_lat, dest_lng, dest_tiers)
        if src_tier is not None and dest_tier is not None:
            res = self.filter_by_dist(src_lat, src_lng, dest_lat, dest_lng, src_tier, dest_tier, "tier", dist)
            if len(res) > 0:
                self.get_cost(res["legs"], float(res["time"]))
                routes.append(res)

        # Get Voi Scooters
        src_vois = voi_service.get_vehicles(src_lat, src_lng, DISTANCE_TO_VEHICLE_LIMIT)
        src_voi = self.closest_location(src_lat, src_lng, src_vois)
        dest_vois = voi_service.get_vehicles(dest_lat, dest_lng, DISTANCE_TO_VEHICLE_LIMIT)
        dest_voi = self.closest_location(dest_lat, dest_lng, dest_vois)
        if src_voi is not None and dest_voi is not None:
            res = self.filter_by_dist(src_lat, src_lng, dest_lat, dest_lng, src_voi, dest_voi, "voi", dist)
            if len(res) > 0:
                self.get_cost(res["legs"], float(res["time"]))
                routes.append(res)

        return routes

    # Filter out journeys to vehicle locations which increase total journey distance
    def filter_by_dist(self,
                       src_lat: float, src_lng: float,
                       dest_lat: float, dest_lng: float,
                       start: dict, drop_off: dict,
                       mode: str, orig_dist: float) -> dict:

        dist_travelled: float = 0
        legs: List[dict] = []
        res = self.cycle_routes_service.get_route(src_lat, src_lng, start["lat"], start["long"])
        leg: dict = {"mode": "walk", "dist": res["distance"], "path": res["path"], "cost": 0}
        dist_travelled += float(res["distance"])
        legs.append(leg)
        res = self.cycle_routes_service.get_route(start["lat"], start["long"], drop_off["lat"],
                                                              drop_off["long"])
        time = self.timing_service.get_travelling_time(res["distance"])
        if mode == "voi" or mode == "tier":
            carbon = self.carbon_service.calculate_carbon_offset(float(dist_travelled), "scooter")
        else:
            carbon = 0
        leg: dict = {"mode": mode, "dist": res["distance"], "path": res["path"]}
        dist_travelled += float(res["distance"])
        legs.append(leg)
        res = self.cycle_routes_service.get_route(drop_off["lat"], drop_off["long"], dest_lat, dest_lng)
        leg: dict = {"mode": "walk", "dist": res["distance"], "path": res["path"], "cost": 0}
        dist_travelled += float(res["distance"])
        legs.append(leg)
        time = self.timing_service.get_travelling_time(dist_travelled)
        dep_time = self.get_dep_time(legs)
        arr_time = self.get_arr_time(time, legs)
        route = {"dep_time": dep_time, "arr_time":  arr_time, "time": time, "emissions": carbon, "dist": dist_travelled, "legs": legs}
        return route

    def get_dep_time(self, legs: list):
        if legs:
            if legs[0].get("dep_time") is not None:
                dep_time = legs[0]["dep_time"]
                return dep_time
        return datetime.datetime.now().astimezone(tz=pytz.timezone("Europe/London")).isoformat()

    def get_arr_time(self, time: str, legs: list):
        if legs:
            if legs[0].get("arr_time") is not None:
                arr_time = legs[-1]["arr_time"]
                return arr_time
        arr_time = datetime.datetime.now().astimezone(tz=pytz.timezone("Europe/London")) + datetime.timedelta(minutes=float(time))
        return arr_time.isoformat()

    # Sorts the list by location and returns the closest location
    def closest_location(self, lat: float, lng: float, locations: list):
        result = sorted(locations, key=lambda k: (hs.haversine((lat, lng), (float(k["lat"]), float(k["long"])))))
        if len(result) >= 1:
            return result[0]
        else:
            return None

    # Get cost of journey given time and mode of transport
    def get_cost(self, legs: List[dict], time: float) -> float:
        for leg in legs:
            if leg["mode"] == "cycle":
                leg["cost"] = (time/30) * 2.00
            elif leg["mode"] == "tier":
                leg["cost"] = 1.00 + (time * 0.15)
            elif leg["mode"] == "voi":
                leg["cost"] = 1.00 + (time * 0.20)


    def find_public_transport(self, src_lat: float, src_lng: float, dest_lat: float, dest_lng: float) -> list:
        try:
            routes = self.public_transport.get_routes(src_lat, src_lng, dest_lat, dest_lng)
            for route in routes:
                route["dep_time"] = self.get_dep_time(route["legs"])
                route["arr_time"] = self.get_arr_time(route["time"], route["legs"])
                route["emissions"] = self.carbon_service.calculate_carbon_offset(float(route["dist"]), "train")
            return routes
        except Exception as e:
            print(format_exc())


if __name__ == "__main__":
    recommendation_service = RecommendedRoutesService()
    res = recommendation_service.get_recommend_routes(51.45591, -2.603067, 51.4665, -2.6122)
    with open("test_output.txt", "w") as file:
        file.write(json.dumps(res))
