from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from app.data_models import Task


class TaskStorage:
    """
    Class used as interface to MongoDB

    Methods
    ---------
    create_task(task: Task): saves a unique task to the collection, returns ValueError if duplicated
    delete_task(task_description: str): remove single task from collection, returns false if not found
    set_task_completed(task_description: str): set task is_completed = true, returns false if not found
    get_all_tasks(): get all tasks in collection, returns a list of app.data_models.Task
    close_storage(): closes db connection
    ---------
    """
    def __init__(self, mongo_uri, database_name):
        self.client = MongoClient(mongo_uri)
        db = self.client[database_name]
        self.collection = db['task']
        self.collection.create_index(['task_description'], unique=True)

    def create_task(self, task: Task):
        """ Save a new unique task in the collection"""
        try:
            inserted_task = self.collection.insert_one(task.model_dump())
            return str(inserted_task.inserted_id)
        except DuplicateKeyError:
            raise ValueError(f"Task '{task.task_description}' already exists.")

    def delete_task(self, task_description: str):
        """ Delete single task from the collection"""
        result = self.collection.delete_one({'task_description': task_description})

        return result.deleted_count > 0

    def set_task_completed(self, task_description: str):
        """ Set task is_completed = True """
        result = self.collection.update_one(
            {'task_description': task_description},
            {'$set': {'is_completed': True}}
        )
        return result.matched_count > 0

    def get_all_tasks(self):
        """ Get all tasks in collection """
        task_data = self.collection.find()
        if task_data:
            return [Task(**task) for task in task_data]
        return None

    def close_storage(self):
        """ Close database connection """
        self.client.close()
