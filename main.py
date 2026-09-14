import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the key
api_key = os.getenv("OPENWEATHER_API_KEY")

API_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city_name: str, api_key: str) -> dict | None:
    """Fetches raw weather data for a given city from OpenWeatherMap API."""
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"  # Options: 'metric' (°C), 'imperial' (°F), 'standard' (K)
    }

    try:
        response = requests.get(API_URL, params=params, timeout=10)
        
        # OpenWeatherMap returns 404 for invalid cities, 401 for bad API keys, etc.
        if response.status_code == 404:
            print(f"Error: City '{city_name}' not found. Please check the spelling.")
            return None
        elif response.status_code == 401:
            print("Error: Invalid API key. Please check your OpenWeatherMap key.")
            return None
        
        # Raise an exception for other HTTP errors (e.g., 500 server errors)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout:
        print("Error: The request timed out. Please check your internet connection.")
    except requests.exceptions.RequestException as err:
        print(f"Error connecting to weather service: {err}")
    
    return None


def display_weather(data: dict) -> None:
    """Parses JSON response and prints relevant weather metrics."""
    city = data.get("name")
    country = data.get("sys", {}).get("country", "")
    
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"].capitalize()
    wind_speed = data["wind"]["speed"]

    print("\n" + "=" * 30)
    print(f" Weather in {city}, {country}")
    print("=" * 30)
    print(f" Condition   : {description}")
    print(f" Temperature : {temp:.1f}°C (Feels like: {feels_like:.1f}°C)")
    print(f" Humidity    : {humidity}%")
    print(f" Wind Speed  : {wind_speed} m/s")
    print("=" * 30 + "\n")


def main():
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        print("Error: OPENWEATHER_API_KEY environment variable not set.")
        print("Please set your API key and try again.")
        sys.exit(1)

    print("--- Basic Weather App ---")
    while True:
        city = input("Enter city name (or 'q' to quit): ").strip()

        if not city:
            continue
        if city.lower() in ("q", "quit", "exit"):
            print("Goodbye!")
            break

        weather_data = get_weather(city, api_key)
        if weather_data:
            display_weather(weather_data)


if __name__ == "__main__":
    main()