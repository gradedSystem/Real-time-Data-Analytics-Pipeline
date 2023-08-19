#Using RapidAPI -> WeatherAPI.com
import http.client

def fetch_data_from_api(api_endpoint):
    conn = http.client.HTTPSConnection("weatherapi-com.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': "828380102bmshff14343f7d12a3bp1d0669jsn24ead0760cd1",
        'X-RapidAPI-Host': "weatherapi-com.p.rapidapi.com"
    }

    conn.request("GET", api_endpoint, headers=headers)

    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")
