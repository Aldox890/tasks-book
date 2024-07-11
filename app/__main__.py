import os
from os import environ
from datetime import datetime

from app.data_models import Task

from app.task_storage import TaskStorage

if __name__ == "__main__":
    try:
        task_storage = TaskStorage(os.environ['MONGO_URI'], 'task_db')
        date_string = '2024-12-27'
        format_datetime = datetime.strptime(date_string, '%Y-%m-%d')

        task1 = Task(task_description="Build-a-snowman", due_date=format_datetime)
        task_storage.create_task(task=task1)

        print(task_storage.get_all_tasks())
        print(task_storage.get_task(task_description="build-a-snowman"))

        if task_storage.delete_task(task_description="Build-a-snowman"):
            print("Task deleted successfully")
        else:
            print("Task does not exists")

    except Exception as e:
        print(e)
