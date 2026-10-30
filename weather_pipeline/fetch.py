# fetch.py
# Original code from section "5.1 Fetch Weather" - moved as-is.
# WORKER layer: talks to the outside world (the API). It needs no other
# project file, because it only produces a plain Python dict.
# DATA OUT: returns response_dict -> main.py passes it to validate.py

from pathlib import Path
import requests
import json

# 5.1 Fetch Weather
def run_weather_fetch() -> dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 29.4241,
        "longitude": -98.4936,
        "current_weather": "true",
    }

    print("Requesting live weather data...")
    response = requests.get(url, params=params)

    print(f"response:\n{response.text}")
    response_text = response.text
    response_dict = json.loads(response_text)

    print(type(response_dict))
    print("RESPONSE\n=================\n",response_dict,"\n=============================")


    print(f"Request URL: {response.url}")
    print(f"Status Code: {response.status_code}")

    output_file = Path("weather_report.json")
    output_file.write_text(response.text, encoding="utf-8")
    print(f"Saved response to {output_file.name}. Open it and find the temperature!")
    return response_dict