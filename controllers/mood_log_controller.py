# Define the REST API endpoints.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from data.database import get_db
from services.mood_log_service import MoodLogService
from services.environment_service import EnvironmentService
from data.repositories import MoodLogRepository
from datetime import datetime


# Define Pydantic models for input/output
class MoodLogInput(BaseModel):
    mood_score: str
    activity: str
    location: Optional[str] = "  default_location"

class MoodLogOutput(BaseModel):
    id: int
    mood_score: str
    activity: str
    weather: str
    air_quality: int
    timestamp: datetime

    class Config:
        orm_mode = True

router = APIRouter(prefix="/api/mood-logs", tags=["Mood Logs"])
mood_log_service = MoodLogService(MoodLogRepository())
environment_service = EnvironmentService()

@router.post("/", response_model=MoodLogOutput)
async def create_mood_log(mood_log_data: MoodLogInput, db: Session = Depends(get_db)):
    """
    Create a new mood log and fetch environmental data (weather and air quality).
    """
    location = mood_log_data.location # request body

    # Fetch weather data to get coordinates
    try:
        weather = await environment_service.fetch_weather(location)
        if weather is None:
            raise HTTPException(status_code=500, detail="Failed to fetch weather data")
        print(f"Weather data fetched: {weather}")  # Debugging line

        # Extract latitude and longitude from the weather response
        lat = weather.get("coord", {}).get("lat")
        lon = weather.get("coord", {}).get("lon")
        if lat is None or lon is None:
            raise HTTPException(status_code=500, detail="Failed to extract coordinates from weather data")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching environmental data: {str(e)}")

    # Fetch air quality data using coordinates
    try:
        air_quality = await environment_service.fetch_air_quality(lat, lon)
        if not air_quality:
            raise HTTPException(status_code=500, detail="Failed to fetch air quality data")
        print(f"Air quality data fetched: {air_quality}")  # Debugging line
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching air quality data: {str(e)}")

    # Add environmental data to the mood log
    mood_log_dict = mood_log_data.dict()
    mood_log_dict["weather"] = weather.get("weather", [{}])[0].get("description", "Unknown")
    mood_log_dict["air_quality"] = air_quality.get("data", {}).get("current", {}).get("pollution", {}).get("aqius", 0)

    # Create the mood log in the database
    try:
        created_log = mood_log_service.create_mood_log(db, mood_log_dict)
        print(f"Mood log created successfully: {created_log}")  # Debugging line
        return created_log
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating mood log: {str(e)}")

@router.get("/", response_model=List[MoodLogOutput])
async def get_all_mood_logs(db: Session = Depends(get_db)):
    """
    Retrieve all mood logs.
    """
    try:
        return mood_log_service.get_all_mood_logs(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching mood logs: {str(e)}")

@router.get("/{log_id}", response_model=MoodLogOutput)
async def get_mood_log_by_id(log_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a mood log by its ID.
    """
    try:
        mood_log = mood_log_service.get_mood_log_by_id(db, log_id)

        if not mood_log:
            raise HTTPException(status_code=404, detail="Mood log not found")
        return mood_log
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching mood log: {str(e)}")