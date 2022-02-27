import haversine as hs
import typing
import math

DISTANCE_LIMIT: float = 10  # meters

"""
{ groups: [
    { lat: x, 
      long: y,
      vehicles: []
    },
    ...
]}
"""


class ClusterService:

    # Proprietary novel super efficient clustering algorithm
    def g_cluster(self, vehicles: list[dict]):
        groups: list[dict] = []
        for vehicle in vehicles:
            group = self.find_closest_group(vehicle["lat"], vehicle["long"], groups)
            if group is not None:
                self.update_group(group, vehicle)
            else:
                groups.append(self.new_group(vehicle))
        return groups

    def find_closest_group(self, lat: float, lng: float, groups: list[dict]) -> typing.Optional[dict]:
        closest_group: dict = None
        min_dist: float = math.inf
        for group in groups:
            dist_to_group = hs.haversine((group["lat"], group["long"]), (lat, lng), unit=hs.Unit.METERS)
            if dist_to_group <= DISTANCE_LIMIT and dist_to_group <= min_dist:
                closest_group = group
                min_dist = dist_to_group

        return closest_group

    def update_group(self, group: dict, new_vehicle: dict) -> None:
        n: int = len(group["vehicles"])
        group["lat"] = (group["lat"] * n + float(new_vehicle["lat"])) / (n + 1)
        group["long"] = (group["long"] * n + float(new_vehicle["long"])) / (n + 1)
        group["vehicles"].append(new_vehicle)

    def new_group(self, vehicle: dict) -> dict:
        return {"lat": vehicle["lat"], "long": vehicle["long"], "vehicles": [vehicle]}


if __name__ == "__main__":
    cluster_service = ClusterService()
