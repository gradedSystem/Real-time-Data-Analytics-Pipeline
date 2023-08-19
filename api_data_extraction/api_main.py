# main.py
from api_handler import fetch_data_from_api
import io, os, json

#list_of_cities
file_path = "list_of_cities.txt"
list_of_cities = []
with open(file_path, "r") as file:
    for line in file:
        list_of_cities.append(line.strip())

astronomy_city_data = [] 
forecast_weather_data = []
"""
List of cities obtaining information through rapidAPI data such as:
1) Sunrise, sunet, moonrise, moonrise, moonset, moon phase and illumation.
2) Forecast weather API method returns upto next 3 days
"""
for cities in list_of_cities:

    #Make API calls
    api_endpoint_1 = "/astronomy.json?q=" + str(cities)
    api_endpoint_2 = "/forecast.json?q=" + str(cities) + "&days=3"

    astronomy_city_data.append(fetch_data_from_api(api_endpoint_1))
    forecast_weather_data.append(fetch_data_from_api(api_endpoint_2))

# Get the path of the 'data' folder in the root directory
data_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
                                
# Create the 'data' folder if it doesn't exist
if not os.path.exists(data_folder_path):
    os.makedirs(data_folder_path)

# Save list as JSON file
astronomy_city_data_json = json.dumps(astronomy_city_data, indent=4)
list_file_path_1 = os.path.join(data_folder_path, "astronomy_city_data.json")
with io.open(list_file_path_1, 'w', encoding='utf-8') as file:
    file.write(astronomy_city_data_json)

print(f"Saved Astronomy data to {list_file_path_1}")

# Save list as JSON file
forecast_weather_data_json = json.dumps(forecast_weather_data, indent=4)
list_file_path_2 = os.path.join(data_folder_path, "forecast_weather_data_json.json")
with io.open(list_file_path_2, 'w', encoding='utf-8') as file:
    file.write(forecast_weather_data_json)

print(f"Saved Forecast data to {list_file_path_2}")