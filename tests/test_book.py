import os

import pytest
from datetime import datetime

from pymongo import MongoClient
from app.data_models import Task
from app.task_storage import TaskStorage

mongo_test_uri = os.environ['MONGO_TEST_URI']
mongo_test_db = os.environ['MONGO_TEST_DB']


@pytest.fixture(scope="module")
def mongo_client():
    client = MongoClient(mongo_test_uri)
    yield client
    client.close()


@pytest.fixture(autouse=True)
def clean_db(mongo_client):
    """ Ensure to clear the database before every unit test """
    print("Cleaning database")
    db = mongo_client[mongo_test_db]
    db.drop_collection('task')


@pytest.fixture(scope="module")
def task_storage():
    task_storage = TaskStorage(mongo_test_uri, mongo_test_db)
    return task_storage


def populated_storage(task_storage):
    """ Populate the database for testing """
    task_storage.create_task(Task(task_description="make-a-snowman", due_date=datetime(2024, 12, 25)))
    task_storage.create_task(Task(task_description="make-a-drink", due_date=datetime(2024, 12, 31)))
    task_storage.create_task(Task(task_description="make-a-firework", due_date=datetime(2025, 1, 29)))


def test_create_task(task_storage):
    """ Entry must be created to pass the test """
    task = Task(task_description="make-a-snowman", due_date=datetime(2024, 12, 25))
    result = task_storage.create_task(task)
    assert result is not None


def test_delete_task(task_storage):
    """ Ony entry must be deleted to pass the test """
    populated_storage(task_storage)
    result = task_storage.delete_task("make-a-snowman")

    assert result is not None
    assert result is not False


def test_set_completed_task(task_storage):
    """ At least one entry must be edited to pass the test """
    populated_storage(task_storage)
    result = task_storage.set_task_completed("make-a-snowman")

    assert result is not None
    assert result is not False


def test_get_task(task_storage):
    """ Entry must be found to pass the test """
    populated_storage(task_storage)
    result = task_storage.get_task("make-a-snowman")

    assert result is not None
    assert len(result) is not 0


def test_get_all_tasks(task_storage):
    """ At least one entry must be present to pass the test """
    populated_storage(task_storage)
    result = task_storage.get_all_tasks()

    assert result is not None
    assert len(result) is not 0
