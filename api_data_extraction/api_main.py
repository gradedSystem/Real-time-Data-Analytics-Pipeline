import json
import os
import io
from api_handler import fetch_data_from_api

LIST_OF_CITIES_FILE = "list_of_cities.txt"
DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

def read_list_of_cities(file_path):
    cities = []
    with open(file_path, "r") as file:
        for line in file:
            cities.append(line.strip())
    return cities

def fetch_astronomy_and_forecast_data(cities):
    astronomy_city_data = []
    forecast_weather_data = []
    
    for city in cities:
        api_endpoint_1 = f"/astronomy.json?q={city}"
        api_endpoint_2 = f"/forecast.json?q={city}&days=3"

        astronomy_data = fetch_data_from_api(api_endpoint_1)
        forecast_data = fetch_data_from_api(api_endpoint_2)

        astronomy_city_data.append(json.loads(astronomy_data))
        forecast_weather_data.append(json.loads(forecast_data))
    
    return astronomy_city_data, forecast_weather_data

def save_json_to_file(data, filename):
    file_path = os.path.join(DATA_FOLDER, filename)
    data_json = json.dumps(data, indent=2)
    with io.open(file_path, 'w', encoding='utf-8') as file:
        file.write(data_json)
    print(f"Saved {filename} to {file_path}")

def main():
    list_of_cities = read_list_of_cities(LIST_OF_CITIES_FILE)
    astronomy_city_data, forecast_weather_data = fetch_astronomy_and_forecast_data(list_of_cities)
    
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    
    save_json_to_file(astronomy_city_data, "astronomy_city_data.json")
    save_json_to_file(forecast_weather_data, "forecast_weather_data.json")

if __name__ == "__main__":
    main()
