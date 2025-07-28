# Repositories interact directly with the database.

from sqlalchemy.orm import Session
from data.models import MoodLog

class MoodLogRepository:
    @staticmethod
    def create_mood_log(db: Session, mood_log_data: dict) -> MoodLog:
        # mood_log = MoodLog(**mood_log_data)
        # db.add(mood_log)
        # db.commit()
        # db.refresh(mood_log)
        # return mood_log
        try: 
            print(f"Creating mood log with data: {mood_log_data}")  # Debugging line
            # create a new lmood log instance
            mood_log = MoodLog(
                mood_score=mood_log_data.get("mood_score"),
                activity=mood_log_data.get("activity"),
                weather=mood_log_data.get("weather"),
                air_quality=mood_log_data.get("air_quality")
            )
            print(f"Prepared mood log instance: {mood_log}")  # Debugging line
            db.add(mood_log) # add the session
            print(f"Added mood log to session")  # Debugging line

            db.commit() # commit the transaction to the database
            print(f"Committed mood log to database")  # Debugging line

            db.refresh(mood_log) # refresh to get the updated instance
            print(f"Refreshed mood log instance: {mood_log}")  # Debugging line

            return mood_log
        except Exception as e:
            print(f"Error in create_mood_log: {e}")  # Debugging line
            raise e

    @staticmethod
    def get_all_mood_logs(db: Session):
        return db.query(MoodLog).order_by(MoodLog.timestamp.desc()).all()

    @staticmethod
    def get_mood_log_by_id(db: Session, log_id: int) -> MoodLog:
        return db.query(MoodLog).filter(MoodLog.id == log_id).first()