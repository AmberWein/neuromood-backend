from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base
from datetime import datetime

class MoodLog(Base):
    __tablename__ = "mood_logs"

    id = Column(Integer, primary_key=True, index=True)
    mood_score = Column(String, nullable=False)
    activity = Column(String, nullable=True)
    weather = Column(String, nullable=False) # Store weather description
    air_quality = Column(Integer, nullable=False) # Store air quality index
    timestamp = Column(DateTime, default=datetime.utcnow)