from .service import Service
from datetime import datetime
from typing import Union
import requests

class WeatherService(Service):

    def __init__(self, api_app_keyname: str = None, api_key_keyname: str = None) -> None:
        super().__init__(api_app_keyname, api_key_keyname)
        self.api_host = "http://api.openweathermap.org/data/2.5"
    
    def get_weather(self, long: float, lat: float) -> Union[dict, int]:
        """
        Get weather data from OpenWeatherMap
        """
        url = f"{self.api_host}/weather"
        query_params = {
            "lat": lat,
            "lon": long,
            "units": "metric",
            "appid": self.app_key,
        }
        r = requests.get(url, params=query_params)
        results = r.json()
        if r.status_code == 200:
            return {
                "temp": results["main"]["temp"],
                "aqi": 1.0,
                "humidity": results["main"]["humidity"],
                "icon_url": f"http://openweathermap.org/img/wn/{results['weather'][0]['icon']}@2x.png",
                "description": results["weather"][0]["main"],
                "description_detailed": results["weather"][0]["description"],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }, r.status_code
        else:
            return results, r.status_code

    def recommend_transport(self, long: float, lat: float):
        weather, ok = self.get_weather(long, lat)
        if ok != 200:
            return None
        t = weather["description"]
        if t == "Snow" or t == "Extreme":
            return f"The weather is {t}. Consider taking a Bus or a Train"
        if t == "Rain":
            return f"It's raining. Maybe bring a coat and be careful if you are cycling or walking"



if __name__ == "__main__":
    weather_service = WeatherService(api_app_keyname="weather", api_key_keyname="OPENWEATHERAPIKEY")
    print(weather_service.get_weather(long=51.45, lat=-2.001))