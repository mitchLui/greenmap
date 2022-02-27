class TimingService:
    # Timing Service for scooters and bikes
    def __init__(self) -> None:
        self.scooting_cycling_speed = 20000/60

    def get_travelling_time(self, distance: str) -> float:
        # distance is in km
        return distance / self.scooting_cycling_speed
        