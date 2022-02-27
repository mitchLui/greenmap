from cycle_routes import CycleRoutesService
from santander_cycles import SantanderCycles
from tier_scooters import TierScooterService

DISTANCE_TO_VEHICLE_LIMIT = 500

class RecommendedRoutesService:

    # Given current coordinates and destination coordinates returns a list of routes with emission and time scores
    def get_recommend_routes(self, src_lat: float, src_lng: float, dest_lat: float, dest_lng: float):
        pass

    def get_separate_rotes(self, src_lat: float, src_lng: float, dest_lat: float, dest_lng: float):
        cycle_service = CycleRoutesService()
        cycle_route = cycle_service.get_route(src_lat, src_lng, dest_lat, dest_lng)

    def find_cycling_vehicles(self, src_lat: float, src_lng: float, dest_lat: float, dest_lng: float):
        cycle_service = SantanderCycles()
        cycle_service.get_cycles(src_lat, src_lng, DISTANCE_TO_VEHICLE_LIMIT)
        tier_service = TierScooterService("", "TIERAPIKEY")
        tier_service.get_scooters(src_lat, src_lng, DISTANCE_TO_VEHICLE_LIMIT)
