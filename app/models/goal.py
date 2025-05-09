from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from sqlalchemy import ForeignKey
from typing import Optional

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")

    @classmethod
    def from_dict(cls, goal_data):
        goal = cls(title=goal_data["title"])

        if "tasks" in goal_data:
            goal.tasks = goal_data["tasks"]
        return goal

    
    def to_dict(self):
        goal_as_dict = {
            "id": self.id,
            "title": self.title,
        }

        # if self.tasks:
        #     goal_as_dict["task_ids"] = [task.id for task in self.tasks]

        return goal_as_dict
