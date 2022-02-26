from service import Service
import requests

CHARGERSURL = "https://api.openchargemap.io/v3/poi/"


def filer_chargers(chargers):
    filtered_chargers = []
    for c in chargers:
        address_info = c.get("AddressInfo", None)
        if address_info is not None and "Latitude" in address_info and "Longitude" in address_info:
            filtered_chargers.append({
                "Location": {
                    "Latitude": address_info["Latitude"],
                    "Longitude": address_info["Longitude"],
                    "AccessComments": address_info.get("AccessComments", "")
                },
                "Chargers": {
                    "Spaces": c.get("NumberOfPoints", "Unknown"),
                    "Connections": c.get("Connections", "Unknown")
                }
            })
    return filtered_chargers

class ChargingService(Service):
    def __init__(self, api_key_keyname: str = None) -> None:
        super().__init__("", api_key_keyname)

    def get_chargers(self, lat: float, lon: float, r: float) -> list:
        params: dict[str, str]
        params = {"output": "json", "countrycode": "GB", "maxresults": "100", "compact": "true", "verbose": "false",
                  "latitude": str(lat), "longitude": str(lon), "distance": str(r), "key": self.app_key}
        r = requests.get(CHARGERSURL, params)
        return filer_chargers(r.json()) if r.status_code == 200 else None


if __name__ == "__main__":
    train_service = ChargingService("CHARGERAPIAPPKEY")
    print(train_service.get_chargers(51.455795, -2.602835, 10))
