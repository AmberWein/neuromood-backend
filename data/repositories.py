# Repositories interact directly with the database.

from sqlalchemy.orm import Session
from data.models import MoodLog

class MoodLogRepository:
    @staticmethod
    def create_mood_log(db: Session, mood_log_data: dict) -> MoodLog:
        mood_log = MoodLog(**mood_log_data)
        db.add(mood_log)
        db.commit()
        db.refresh(mood_log)
        return mood_log

    @staticmethod
    def get_all_mood_logs(db: Session):
        return db.query(MoodLog).order_by(MoodLog.timestamp.desc()).all()

    @staticmethod
    def get_mood_log_by_id(db: Session, log_id: int) -> MoodLog:
        return db.query(MoodLog).filter(MoodLog.id == log_id).first()