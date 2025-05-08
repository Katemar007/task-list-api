from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]

    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data["title"]
        )
    
    def to_dict(self):
        task_as_dict = {
            "id": self.id,
            "title": self.title,
    }
        
        return task_as_dict