from pydantic import BaseModel
from datetime import datetime


class Task(BaseModel):
    """ Data model for single task """
    task_description: str
    due_date: datetime
    is_completed: bool = False
