# # Create a separate service for external API calls.

# import httpx
# import os
# from typing import Optional
# from dotenv import load_dotenv

# load_dotenv()

# class EnvironmentService:
#     def __init__(self):
#         self.openweather_key = os.getenv("OPENWEATHER_KEY")
#         self.iqair_key = os.getenv("IQAIR_KEY")

#     async def fetch_weather(self, location: str) -> Optional[dict]:
#         url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.openweather_key}"
#         async with httpx.AsyncClient() as client:
#             try:
#                 response = await client.get(url)
#                 response.raise_for_status()  # Raise an exception for HTTP errors
#                 return response.json()
#             except httpx.HTTPStatusError as e:
#                 print(f"HTTP error: {e}")
#             except Exception as e:
#                 print(f"Unexpected error: {e}")
#         return None

#     async def fetch_air_quality(self, lat: float, lon: float) -> Optional[dict]:
#         url = f"https://api.airvisual.com/v2/nearest_city?lat={lat}&lon={lon}&key={self.iqair_key}"
#         async with httpx.AsyncClient() as client:
#             response = await client.get(url)
#             if response.status_code == 200:
#                 return response.json()
#             return None

import httpx
import os
from typing import Optional
from dotenv import load_dotenv
import logging

# Load environment variables from .env
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnvironmentService:
    def __init__(self):
        self.openweather_key = os.getenv("OPENWEATHER_KEY")
        self.iqair_key = os.getenv("IQAIR_KEY")

    async def fetch_weather(self, location: str) -> Optional[dict]:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.openweather_key}"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                response.raise_for_status()  # Check for HTTP errors
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error: {e}")
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
        return None

    async def fetch_air_quality(self, lat: float, lon: float) -> Optional[dict]:
        url = f"https://api.airvisual.com/v2/nearest_city?lat={lat}&lon={lon}&key={self.iqair_key}"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                response.raise_for_status()  # Raise an exception for HTTP errors
                logger.info(f"Fetched air quality data for coordinates ({lat}, {lon}): {response.status_code}")
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error while fetching air quality data for coordinates ({lat}, {lon}): {e}")
            except Exception as e:
                logger.error(f"Unexpected error while fetching air quality data for coordinates ({lat}, {lon}): {e}")
        return None