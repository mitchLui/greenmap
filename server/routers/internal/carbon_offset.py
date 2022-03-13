from typing import List, Union


class CarbonOffsetCalculator:

    def __init__(self) -> None:
        # carbon emitted per km
        self.carbon_emissions = {
            "scooter": 0.11,
            "bus": 0.89,
            "train": 0.035,
            "ev": 33
        }


    def calculate_carbon_offset(self, distance: float, type: str) -> float:
        if self.carbon_emissions.get(type) is not None:
            return round(self.carbon_emissions[type] * distance, 2)
        else:
            raise Exception("Unknown type")

    def calculate_carbon_offset_list(self, distances: List[float], types: List[str]) -> Union[float, float]:
        # NOTE: distances is in metres
        # Convert back to km
        distances = [d / 1000 for d in distances]
        carbon_offset = 0
        if len(distances) != len(types):
            raise Exception("The number of distances and types must be the same")
        for i in range(len(distances)):
            carbon_offset += self.calculate_carbon_offset(distances[i], types[i])
        return round(carbon_offset, 2), sum(distances)

if __name__ == "__main__":
    co = CarbonOffsetCalculator()
    print(co.calculate_carbon_offset(2000, "scooter"))
    #print(co.calculate_carbon_offset(10, "bus"))
    #print(co.calculate_carbon_offset(10, "train"))
    #print(co.calculate_carbon_offset(10, "ev"))
    print(co.calculate_carbon_offset_list([10, 10, 10, 10], ["scooter", "bus", "train", "ev"]))
