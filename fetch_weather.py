import requests
import logging
from dotenv import load_dotenv
import os


load_dotenv()

#create a logger
logger = logging.getLogger("weather_appi_logger")

#set logger level to Error
logger.setLevel(logging.DEBUG)

#Create formmatters and add them to handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


#Dictionary to store cached APIs
weather_cache = {}


def fetch_weather (city,api_key):
    logger.info(f"fetching weather data for {city}")
    city = city.strip().lower() #normalize city names

    #check if data is already cached
    if city in weather_cache:
        logger.info(f"fetching cached weather data ")
        return weather_cache[city]
    
    #fetch data fro API
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            weather_info = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "weather":data["weather"][0]["description"],
            }
            #store response in cache
            weather_cache[city] = weather_info
            logger.info(f"Weather in {city}: {weather_info}")
            return weather_info
        else:
            return {"error": "could not fetch weather data"}
        
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError:
        logger.critical("Network error! Check your connection.")
    except requests.exceptions.Timeout:
        logger.warning("Request timed out. Try again later.")
    except requests.exceptions.RequestException as err:
        logger.error(f"Unexpected error: {err}")

if __name__ == "__main__":

    API_KEY = os.getenv("WEATHER_API_KEY")

    city_name = input("Enter city name:")

    weather_data = fetch_weather(city_name, API_KEY)

    print(weather_data)


