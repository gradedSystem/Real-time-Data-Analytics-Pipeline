#Using RapidAPI -> WeatherAPI.com
import http.client
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")

def fetch_data_from_api(api_endpoint):
    conn = http.client.HTTPSConnection(RAPIDAPI_HOST)

    headers = {
        'X-RapidAPI-Key': RAPIDAPI_KEY,
        'X-RapidAPI-Host': RAPIDAPI_HOST
    }

    conn.request("GET", api_endpoint, headers=headers)

    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")