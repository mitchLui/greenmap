from .service import Service
import requests

CHARGERSURL = "https://api.openchargemap.io/v3/poi/"

class ChargingService(Service):
    def __init__(self, api_key_keyname: str = None) -> None:
        super().__init__("", api_key_keyname)

    def filter_chargers(self, chargers):
        filtered_chargers = []
        for c in chargers:
            address_info = c.get("AddressInfo", None)
            if address_info is not None and "Latitude" in address_info and "Longitude" in address_info:
                connections = c.get("Connections", "Unknown")
                if connections != "Unknown":
                    connections = [
                        {
                            x.lower(): y
                        } for connection in connections for x, y in connection.items()
                    ]
                filtered_chargers.append(
                    {
                        "long": address_info["Longitude"],
                        "lat": address_info["Latitude"],
                        "access_comments": address_info.get("AccessComments", ""),
                        "chargers": {
                            "spaces": c.get("NumberOfPoints", "Unknown"),
                            "connections": connections
                        }
                    }
                )
        return filtered_chargers

    def get_chargers(self, lat: float, lon: float, r: float) -> list:
        params: dict[str, str]
        params = {"output": "json", "countrycode": "GB", "maxresults": "100", "compact": "true", "verbose": "false",
                  "latitude": str(lat), "longitude": str(lon), "distance": str(r), "key": self.app_key}
        r = requests.get(CHARGERSURL, params)
        return self.filter_chargers(r.json()) if r.status_code == 200 else []


if __name__ == "__main__":
    train_service = ChargingService("CHARGERAPIAPPKEY")
    print(train_service.get_chargers(51.455795, -2.602835, 10))
