import haversine as hs
import json

from cycle_routes import CycleRoutesService
from santander_cycles import SantanderCycles
from tier_scooters import TierScooterService
from voi import VoiService
from cycle_routes import CycleRoutesService
from timing_service import TimingService
from carbon_offset import CarbonOffsetCalculator

# The acceptable distance to walk to the nearest vehicle
DISTANCE_TO_VEHICLE_LIMIT = 250  # metres

# The acceptable extra distance to the journey to get the vehicle
EXTRA_DISTANCE_TO_GET_VEHICLE = 10  # percentage

# TODO: ADD PUBLIC TRANSPORT
# TODO: MULTITHREADING OR LIMIT TO CLOSEST VEHICLE STATION
# TODO: IMPLEMENT ADD COST FUNCTION

class RecommendedRoutesService:
    def __init__(self):
        self.cycle_routes_service = CycleRoutesService("TRANSPORTAPIAPPID", "TRANSPORTAPIAPPKEY")
        self.timing_service = TimingService()
        self.carbon_service = CarbonOffsetCalculator()

    # Given current coordinates and destination coordinates returns a list of routes with emission and time scores
    def get_recommend_routes(self, src_lat: float, src_lng: float, dest_lat: float, dest_lng: float):
        recommendations = {"routes": []}
        recommendations["routes"] = self.find_cycling_vehicles(src_lat, src_lng, dest_lat, dest_lng)
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
        dest_cycles = cycle_service.get_cycles(dest_lat, dest_lng, DISTANCE_TO_VEHICLE_LIMIT)
        if src_cycles is not None and dest_cycles is not None:
            res = self.filter_by_dist(src_lat, src_lng, dest_lat, dest_lng, src_cycles, dest_cycles,"cycle", dist)
            if len(res) > 0:
                routes.extend(res)

        # Get TIER Scooters
        src_tiers = tier_service.get_scooters(src_lat, src_lng, DISTANCE_TO_VEHICLE_LIMIT)
        dest_tiers = tier_service.get_scooters(dest_lat, dest_lng, DISTANCE_TO_VEHICLE_LIMIT)
        if src_tiers is not None and dest_tiers is not None:
            res = self.filter_by_dist(src_lat, src_lng,dest_lat, dest_lng, src_tiers, dest_tiers,"tier", dist)
            if len(res) > 0:
                routes.extend(res)

        # Get Voi Scooters
        src_vois = voi_service.get_vehicles(src_lat, src_lng, DISTANCE_TO_VEHICLE_LIMIT)
        dest_vois = voi_service.get_vehicles(dest_lat, dest_lng, DISTANCE_TO_VEHICLE_LIMIT)
        if src_vois is not None and dest_vois is not None:
            res = self.filter_by_dist(src_lat, src_lng,dest_lat, dest_lng,src_vois, dest_vois,"voi", dist)
            if len(res) > 0:
                routes.extend(res)

        return routes

    # Filter out journeys to vehicle locations which increase total journey distance
    def filter_by_dist(self,
                       src_lat: float, src_lng: float,
                       dest_lat: float, dest_lng: float,
                       starts: list[dict], drop_offs: list[dict],
                       mode: str, orig_dist: float) -> list:

        routes: list = []
        for start in starts:
            src_to_vehicle = hs.haversine((src_lat, src_lng), (float(start["lat"]), float(start["long"])))
            for drop_off in drop_offs:
                vehicle_to_drop = hs.haversine((float(start["lat"]), float(start["long"])), (float(drop_off["lat"]), float(drop_off["long"])), unit=hs.Unit.METERS)
                drop_to_dest = hs.haversine((float(drop_off["lat"]), float(drop_off["long"])), (dest_lat, dest_lng), unit=hs.Unit.METERS)
                total_dist = src_to_vehicle + vehicle_to_drop + drop_to_dest
                if ((total_dist - orig_dist) / orig_dist) <= EXTRA_DISTANCE_TO_GET_VEHICLE/100:
                    dist_travelled: float = 0
                    legs: list[dict] = []
                    res = self.cycle_routes_service.get_route(src_lat, src_lng, start["lat"], start["long"])
                    leg: dict = {"mode": "walk", "dist": res["distance"], "path": res["path"], "cost": 0}
                    dist_travelled += float(res["distance"])
                    legs.append(leg)
                    res = self.cycle_routes_service.get_route(start["lat"], start["long"], drop_off["lat"],
                                                              drop_off["long"])
                    time = self.timing_service.get_travelling_time(res["distance"])
                    cost = self.get_cost(time, mode)
                    if mode == "voi" or mode == "tier":
                        carbon = self.carbon_service.calculate_carbon_offset(float(dist_travelled), "scooter")
                    else:
                        carbon = 0
                    leg: dict = {"mode": mode, "dist": res["distance"], "path": res["path"], "cost": cost}
                    dist_travelled += float(res["distance"])
                    legs.append(leg)
                    res = self.cycle_routes_service.get_route(drop_off["lat"], drop_off["long"], dest_lat, dest_lng)
                    leg: dict = {"mode": "walk", "dist": res["distance"], "path": res["path"], "cost": 0}
                    dist_travelled += float(res["distance"])
                    legs.append(leg)
                    time = self.timing_service.get_travelling_time(dist_travelled)
                    route = {"time": time, "emissions": carbon, "dist": dist_travelled, "legs": legs}
                    routes.append(route)

        return routes

    # Get cost of journey given time and mode of transport
    def get_cost(self, time: float, mode: str) -> float:
        # TODO: Get cost based on mode of transport
        """
        if mode == "cycle":
        elif mode == "tier":
        elif mode == "voi":
        """
        return None


if __name__ == "__main__":
    recommendation_service = RecommendedRoutesService()
    res = recommendation_service.get_recommend_routes(51.45591, -2.603067, 51.4665, -2.6122)
    with open("test_output.txt", "w") as file:
        file.write(json.dumps(res))