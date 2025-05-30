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

        return goal

    def goal_with_tasks(self):
        task_list = []

        for task in self.tasks:
            task = task.to_dict()
            task["goal_id"] = self.id
            task_list.append(task)
        
        goal_with_tasks = self.to_dict()
        goal_with_tasks["tasks"] = task_list

        return goal_with_tasks
    
    def to_dict(self):
        goal_as_dict = {
            "id": self.id,
            "title": self.title,
        }

        # if self.tasks:
        #     goal_as_dict["task_ids"] = [task.id for task in self.tasks]

        return goal_as_dict
