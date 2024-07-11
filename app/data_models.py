from pydantic import BaseModel
from datetime import datetime


class Task(BaseModel):
    task_description: str
    due_date: datetime
    is_completed: bool = False
