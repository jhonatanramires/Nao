from langchain.agents import tool
import openmeteo_requests
import requests
from typing import Dict, Any, Optional

openmeteo = openmeteo_requests.Client()

@tool
def get_weather_data(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Fetches weather data from the Open-Meteo API and returns the weather details as a dictionary.
    
    Args:
    latitude (float): The latitude of the location
    longitude (float): The longitude of the location
    
    Returns:
    Dict[str, Any]: A dictionary containing current weather data
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain", "showers", "snowfall"]
    }
    try:
        responses = openmeteo.weather_api(url, params=params)
        current_weather = responses[0].Current()
        return {var.Name(): var.Value() for var in current_weather.Variables()}
    except Exception as e:
        return {"error": str(e)}

def get_weather_info(info_type: str, latitude: float, longitude: float) -> str:
    """
    Helper function to get specific weather information.
    
    Args:
    info_type (str): The type of weather information to retrieve
    latitude (float): The latitude of the location
    longitude (float): The longitude of the location
    
    Returns:
    str: Formatted weather information
    """
    weather_data = get_weather_data(latitude, longitude)
    if "error" in weather_data:
        return f"Error fetching weather data: {weather_data['error']}"
    
    info_mapping = {
        "temperature": ("temperature_2m", "Temperature", "°C"),
        "humidity": ("relative_humidity_2m", "Relative Humidity", "%"),
        "apparent_temperature": ("apparent_temperature", "Apparent Temperature", "°C"),
        "precipitation": ("precipitation", "Precipitation", "mm"),
        "rain": ("rain", "Rain", "mm"),
        "showers": ("showers", "Showers", "mm"),
        "snowfall": ("snowfall", "Snowfall", "mm")
    }
    
    if info_type in info_mapping:
        key, label, unit = info_mapping[info_type]
        return f"{label}: {weather_data.get(key, 'N/A')}{unit}"
    elif info_type == "day_night":
        return "It is currently day." if weather_data.get("is_day", 0) else "It is currently night."
    else:
        return f"Unknown information type: {info_type}"

@tool
def get_temperature(latitude: float, longitude: float) -> str:
    """
    Returns the temperature at 2 meters height for the specified location.
    """
    return get_weather_info("temperature", latitude, longitude)

@tool
def get_relative_humidity(latitude: float, longitude: float) -> str:
    """
    Returns the relative humidity at 2 meters height for the specified location.
    """
    return get_weather_info("humidity", latitude, longitude)

@tool
def get_apparent_temperature(latitude: float, longitude: float) -> str:
    """
    Returns the apparent temperature for the specified location.
    """
    return get_weather_info("apparent_temperature", latitude, longitude)

@tool
def get_day_or_night(latitude: float, longitude: float) -> str:
    """
    Returns whether it is currently day or night at the specified location.
    """
    return get_weather_info("day_night", latitude, longitude)

@tool
def get_precipitation(latitude: float, longitude: float) -> str:
    """
    Returns the precipitation level for the specified location.
    """
    return get_weather_info("precipitation", latitude, longitude)

@tool
def get_rain(latitude: float, longitude: float) -> str:
    """
    Returns the rain level for the specified location.
    """
    return get_weather_info("rain", latitude, longitude)

@tool
def get_showers(latitude: float, longitude: float) -> str:
    """
    Returns the showers level for the specified location.
    """
    return get_weather_info("showers", latitude, longitude)

@tool
def get_snowfall(latitude: float, longitude: float) -> str:
    """
    Returns the snowfall level for the specified location.
    """
    return get_weather_info("snowfall", latitude, longitude)

@tool
def get_full_weather_report(latitude: float, longitude: float) -> str:
    """
    Returns a full weather report for the specified location.
    """
    weather_data = get_weather_data(latitude, longitude)
    if "error" in weather_data:
        return f"Error fetching weather data: {weather_data['error']}"
    
    report = [
        f"Weather Report for coordinates ({latitude}, {longitude}):",
        get_temperature(latitude, longitude),
        get_relative_humidity(latitude, longitude),
        get_apparent_temperature(latitude, longitude),
        get_day_or_night(latitude, longitude),
        get_precipitation(latitude, longitude),
        get_rain(latitude, longitude),
        get_showers(latitude, longitude),
        get_snowfall(latitude, longitude)
    ]
    return "\n".join(report)