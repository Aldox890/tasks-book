from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from app.data_models import Task


class TaskStorage:

    def __init__(self, mongo_uri, database_name):
        self.client = MongoClient(mongo_uri)
        db = self.client[database_name]
        self.collection = db['task']
        self.collection.create_index(['task_description'], unique=True)

    def create_task(self, task: Task):
        try:
            inserted_task = self.collection.insert_one(task.model_dump())
            return str(inserted_task.inserted_id)
        except DuplicateKeyError:
            raise ValueError(f"Task '{task.task_description}' already exists.")

    def delete_task(self, task_description: str):
        result = self.collection.delete_one({'task_description': task_description})
        return result.deleted_count > 0

    def set_task_completed(self, task_description: str):
        result = self.collection.update_one(
            {'task_description': task_description},
            {'$set': {'is_completed': True}}
        )
        return result.matched_count > 0

    def get_task(self, task_description: str):
        task_data = self.collection.find({'task_description': task_description})
        if task_data:
            return [Task(**task) for task in task_data]
        return None

    def get_all_tasks(self):
        task_data = self.collection.find()
        if task_data:
            return [Task(**task) for task in task_data]
        return None

    def close_storage(self):
        self.client.close()
