from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from datetime import datetime
from ..db import db

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data["title"], 
            description=task_data["description"],
            completed_at=task_data.get("completed_at")
        )

        # new_task = Task(title=task_data["title"], 
        # description=task_data["description"],
        # completed_at=task_data["completed_at"])
        # return new_task
    
    def to_dict(self, include_completed_at=False):
        task_as_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at)
    }

        if include_completed_at:
            task_as_dict["completed_at"] = self.completed_at

        return task_as_dict