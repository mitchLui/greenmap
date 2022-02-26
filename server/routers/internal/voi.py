from service import Service
import time
import os
import requests
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import math
from apscheduler.schedulers.background import BackgroundScheduler
import haversine as hs  # used for distance calculations between coordinates


VOIAPIUPDATEURL = "https://api.voiapp.io/v1/auth/session"
VOIAPIZONEURL = "https://api.voiapp.io/v1/zones"
VOIAPIVEHICLES = "https://api.voiapp.io/v2/rides/vehicles"


# code taken from https://stackoverflow.com/questions/53075481/how-do-i-cluster-a-list-of-geographic-points-by-distance
def distance(origin, destination):  # found here https://gist.github.com/rochacbruno/2883505
    lat1, lon1 = origin[0], origin[1]
    lat2, lon2 = destination[0], destination[1]
    radius = 6371  # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d


def create_clusters(number_of_clusters, points):
    kmeans = KMeans(n_clusters=number_of_clusters, random_state=0).fit(points)
    l_array = np.array([[label] for label in kmeans.labels_])
    clusters = np.append(points, l_array, axis=1)
    return clusters


def validate_solution(max_dist, clusters):
    _, __, n_clust = clusters.max(axis=0)
    n_clust = int(n_clust)
    for i in range(n_clust):
        two_d_cluster = clusters[clusters[:, 2] == i][:, np.array([True, True, False])]
        if not validate_cluster(max_dist, two_d_cluster):
            return False
        else:
            continue
    return True


def validate_cluster(max_dist, cluster):
    distances = cdist(cluster, cluster, lambda ori, des: int(round(distance(ori, des))))
    print(distances)
    print(30 * '-')
    for item in distances.flatten():
        if item > max_dist:
            return False
    return True


class VoiService(Service):

    def update_api_key(self):
        success = False
        response = None
        while not success:
            body = f'{{"authenticationToken": "{self.app_id}"}}'
            r = requests.post(VOIAPIUPDATEURL, data=body)
            success = r.status_code == 200
            response = r.json()
        self.app_id = response["authenticationToken"]
        self.app_key = response["accessToken"]

    def __init__(self, api_app_keyname: str = None) -> None:
        super().__init__(api_app_keyname, "")
        # scheduler = BackgroundScheduler()
        # scheduler.add_job(self.update_api_key, 'interval', minutes=8)
        # scheduler.start()
        self.update_api_key()

    def get_vehicles(self, zone_id: int):
        print(zone_id)
        r = requests.get(VOIAPIVEHICLES, {"zone_id": zone_id}, headers={"x-access-token": self.app_key})
        print(r.text)

    def get_zones(self, lat: float, lon: float) -> dict:
        r = requests.get(VOIAPIZONEURL, {"lat": lat, "lng": lon}, headers={"x-access-token": self.app_key})
        if r.status_code != 200:
            return None
        for zone in r.json()["zones"]:
            boundaries = zone["boundaries"]
            if boundaries["Lo"]["Lat"] <= lat <= boundaries["Hi"]["Lat"] and boundaries["Lo"]["Lng"] <= lon <= \
                    boundaries["Hi"]["Lng"]:
                return {"zone_id": zone["zone_id"], "start_cost": zone["start_cost"],
                        "minute_cost": zone["minute_cost"]}
        return None


if __name__ == "__main__":
    voi_service = VoiService("VOIAPIAUTHTOCKEN")
    voi_service.get_vehicles(voi_service.get_zones(51.4545, -2.5879)["zone_id"])
