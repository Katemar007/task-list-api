from sqlalchemy.orm import Mapped, mapped_column, column_property, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from sqlalchemy import DateTime
from datetime import datetime
from ..db import db

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    is_complete = column_property(completed_at != None)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    @classmethod
    def from_dict(cls, task_data):
        goal_id=task_data.get("goal_id")
        completed_at = task_data.get("completed_at", None)
        
        return cls(
            title=task_data["title"], 
            description=task_data["description"],
            completed_at = completed_at,
            goal_id=goal_id
            )

    
    def to_dict(self, include_completed_at=False):
        task_as_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.is_complete)
    }

        if include_completed_at:
            task_as_dict["completed_at"] = self.completed_at
        
        if self.goal:
            task_as_dict["goal_id"] = self.goal.id

        return task_as_dict