# Services abstract the logic and ensure reusability across controllers.

from data.repositories import MoodLogRepository
from sqlalchemy.orm import Session

class MoodLogService:
    def __init__(self, repository: MoodLogRepository):
        self.repository = repository

    def create_mood_log(self, db: Session, mood_log_data: dict):
        return self.repository.create_mood_log(db, mood_log_data)

    def get_all_mood_logs(self, db: Session):
        return self.repository.get_all_mood_logs(db)

    def get_mood_log_by_id(self, db: Session, log_id: int):
        return self.repository.get_mood_log_by_id(db, log_id)