#* PRIVATE
from operator import invert
from tokenize import group
import haversine as hs
from typing import Optional, List
from loguru import logger
import math
from .unionFind import UnionFind
import itertools

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

# def new_group(vehicle: dict) -> dict:
#     return {"lat": vehicle["lat"], "long": vehicle["long"], "vehicles": [vehicle]}


# def update_group(group: dict, new_vehicle: dict) -> None:
#     n: int = len(group["vehicles"])
#     group["lat"] = (group["lat"] * n + float(new_vehicle["lat"])) / (n + 1)
#     group["long"] = (group["long"] * n + float(new_vehicle["long"])) / (n + 1)
#     group["vehicles"].append(new_vehicle)


# def find_closest_group(lat: float, lng: float, groups: List[dict]) -> Optional[dict]:
#     closest_group: dict = None
#     min_dist: float = math.inf
#     for group in groups:
#         dist_to_group = hs.haversine((group["lat"], group["long"]), (lat, lng), unit=hs.Unit.METERS)
#         if dist_to_group <= DISTANCE_LIMIT and dist_to_group <= min_dist:
#             closest_group = group
#             min_dist = dist_to_group

#     return closest_group

# # Proprietary novel super efficient clustering algorithm
# def g_cluster(vehicles: List[dict]):
#     groups: List[dict] = []
#     for vehicle in vehicles:
#         group = find_closest_group(vehicle["lat"], vehicle["long"], groups)
#         if group is not None:
#             update_group(group, vehicle)
#         else:
#             groups.append(new_group(vehicle))
#     return groups

def vehicleDistance(v1, v2):
    return  hs.haversine((v1["lat"], v1["long"]), (v2["lat"], v2["long"]), unit=hs.Unit.METERS)

def create_cluster(vehicles: List[dict]) -> dict:
    n = len(vehicles)
    avgLat = sum(v["lat"] for v in vehicles) / n
    avgLong = sum(v["long"] for v in vehicles) / n
    return {"lat": avgLat, "long": avgLong, "vehicles": vehicles}

def oof_cluster(vehicles: List[dict]):
    inverse = {}
    uf = UnionFind(map(lambda v: v["reg"], vehicles))
    for i, v1 in enumerate(vehicles):
        inverse[v1["reg"]] = v1
        for j in range(i + 1, len(vehicles)):
            v2 = vehicles[j]
            if vehicleDistance(v1, v2) < DISTANCE_LIMIT:
                uf.union(v1["reg"], v2["reg"])
    logger.info(inverse)
    groups = list(map(lambda g: list(map(lambda reg: inverse.get(reg), g)), uf.getGroups()))
    return list(map(create_cluster, groups))
    