from typing import List, Union
import requests

class CarbonOffsetCalculator:

    def __init__(self) -> None:
        #carbon emitted per km
        self.carbon_emissions = {
            "scooter": 0.11,
            "bus": 0.89,
            "train": 35.1,
            "ev": 0.06
        }
        self.recommended_sites = ""


    def calculate_carbon_offset(self, distance: float, type: str) -> float:
        carbon_offset = 0
        if type == "scooter":
            carbon_offset = self.scooter_carbon * distance
        elif type == "bus":
            carbon_offset = self.bus_carbon * distance
        elif type == "train":
            carbon_offset = self.train_carbon * distance
        elif type == "ev":
            carbon_offset = self.ev_carbon * distance
        else:
            raise Exception("Unknown type")
        return round(carbon_offset, 2)

    def calculate_carbon_offset_list(self, distances: List[float], types: List[str]) -> Union[float, float]:
        carbon_offset = 0
        if len(distances) != len(types):
            raise Exception("The number of distances and types must be the same")
        for i in range(len(distances)):
            carbon_offset += self.calculate_carbon_offset(distances[i], types[i])
        return round(carbon_offset, 2), sum(distances)

if __name__ == "__main__":
    co = CarbonOffsetCalculator()
    print(co.calculate_carbon_offset(10, "scooter"))
    print(co.calculate_carbon_offset(10, "bus"))
    print(co.calculate_carbon_offset(10, "train"))
    print(co.calculate_carbon_offset(10, "ev"))
    print(co.calculate_carbon_offset_list([10, 10, 10, 10], ["scooter", "bus", "train", "ev"]))
