# Libraries
import os
import json
from api_handler import fetch_data_from_api
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

COORDINATES_FILE = os.getenv("cord_abs_path")

# Function to read list of coordinates from a file
def read_list_of_coordinates(file_path):
    coordinates = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                lat, lon = line.strip().split(",")
                coordinates.append((float(lat), float(lon)))
    except FileNotFoundError:
        print("Error: The specified file was not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
    return coordinates

# Function to fetch astronomy and forecast data for given coordinates
def fetch_astronomy_and_forecast_data(coordinates):
    real_time_data = []

    try:
        for coord in read_list_of_coordinates(coordinates):
            lat, lon = coord[0], coord[1]
            api_endpoint = f"/current.json?q={lat}%2C{lon}"
            fetch_data = fetch_data_from_api(api_endpoint)
            real_time_data.append(json.loads(fetch_data))
    except Exception as e:
        print(f"An error occurred while fetching data from the API: {e}")

    return real_time_data
