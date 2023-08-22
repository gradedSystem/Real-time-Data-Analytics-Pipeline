# Libraries
import json
from api_handler import fetch_data_from_api
from pathlib import Path

directory = Path("path/to/your/directory")
COORDINATES_FILE = "coordinates.txt"

# Function to read list of coordinates from a file
def read_list_of_coordinates(file_path):
    coordinates = []
    with open(file_path, "r") as file:
        for line in file:
            lat, lon = line.strip().split(",")
            coordinates.append((float(lat), float(lon)))
    return coordinates

# Function to fetch astronomy and forecast data for given coordinates
def fetch_astronomy_and_forecast_data(coordinates):
    real_time_data = []
    
    for coord in coordinates:
        lat, lon = coord
        api_endpoint = f"/current.json?q={lat}%2C{lon}"
        fetch_data = fetch_data_from_api(api_endpoint)
        real_time_data.append(json.loads(fetch_data))
    
    return real_time_data
print(read_list_of_coordinates(COORDINATES_FILE))