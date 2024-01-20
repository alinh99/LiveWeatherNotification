from bs4 import BeautifulSoup
import requests
from win11toast import toast
import time
import schedule
def get_data(url):
    url_request = requests.get(url)
    return url_request.text    

city = "Danang"
soup = BeautifulSoup(get_data(f"https://www.meteoprog.com/weather/{city}/"), "html.parser")

weather_result = {}

today_temp = soup.find("div", "today-temperature").find("span").text
feels_like = soup.find("span", "feels-like").text.strip()
weather_info = soup.find("h3").text
today_atmosphere = soup.find_all("td", "atmosphere-spec")
today_hourly_weather = soup.find("ul", "today-hourly-weather hide-scroll").find_all("li")

weather_result["today_temp"] = today_temp
weather_result["feels_like"] = feels_like
weather_result["weather_info"] = weather_info

for atmosphere in today_atmosphere:
    if atmosphere.find("span").attrs["class"] == ["icon-rain-drops"]:
        rain_chance = atmosphere.find("b").text + "%"
        weather_result["rain_chance"] = rain_chance
    
    if atmosphere.find("span").attrs["class"] == ["icon-wind"]:
        wind = atmosphere.find("b").text + " m/s"
        weather_result["wind"] = wind
    
    if atmosphere.find("span").attrs["class"] == ["icon-meater"]:
        pressure = atmosphere.find("b").text
        weather_result["pressure"] = pressure
    
    if atmosphere.find("span").attrs["class"] == ["icon-uv"]:
        uv = atmosphere.find("b").text
        weather_result["uv"] = uv
    
    if atmosphere.find("span").attrs["class"] == ["icon-dropp"]:
        humidity = atmosphere.find("b").text + "%"
        weather_result["humidity"] = humidity
    
    if atmosphere.find("span").attrs["class"] == ["icon-rainfall"]:
        precipitation = atmosphere.find("b").text
        weather_result["precipitation"] = precipitation

for today_hourly in today_hourly_weather:
    today_hourly_name = today_hourly.find("span", "today-hourly-weather__name").text
    today_hourly_temp = today_hourly.find("span", "today-hourly-weather__temp").text
    today_hourly_feel = today_hourly.find("span", "today-hourly-weather__feel").text
    
    weather_result[f"{today_hourly_name.lower()}_temp"] = today_hourly_temp
    weather_result[f"{today_hourly_name.lower()}_feel"] = today_hourly_feel
    # print(today_hourly_temp)

# print(weather_result)

result = f"""Today Temperature: {weather_result["today_temp"]}
{weather_result["feels_like"]}
Chance of Rain: {weather_result["rain_chance"]} 
"""

def send_notification():
    toast("Weather", result)

send_notification()
schedule.every(1).hour.do(send_notification)

while True:
  schedule.run_pending()
  time.sleep(1)