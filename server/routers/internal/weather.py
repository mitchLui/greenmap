from .service import Service

class WeatherService(Service):
    
    def get_weather(self, long: float, lat: float, radius: float) -> dict:
        pass
