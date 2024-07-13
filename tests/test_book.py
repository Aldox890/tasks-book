import os
import pytest

from pymongo import MongoClient
from app.task_book import TaskBook

mongo_test_uri = os.getenv('MONGO_TEST_URI', 'mongodb://test_usr:test_pwd@localhost:27017/')
mongo_test_db = os.getenv('MONGO_TEST_DB', 'task_db_test')


@pytest.fixture(scope="module")
def mongo_client():
    client = MongoClient(mongo_test_uri)
    yield client
    client.close()


@pytest.fixture(scope="module")
def clean_db(mongo_client):
    """ Ensure to clear the database before every unit test """
    print("Cleaning database")
    db = mongo_client[mongo_test_db]
    db.drop_collection('task')


@pytest.fixture(scope="module")
def tasks_book(clean_db):
    tasks_book = TaskBook(mongo_test_uri, mongo_test_db)
    return tasks_book


def populated_storage(tasks_book):
    """ Populate the database for testing """
    tasks_book.add_task("make-a-snowman", "2024-12-25")
    tasks_book.add_task("make-a-drink", "2024-12-31")
    tasks_book.add_task("make-a-firework", "2025-1-29")


def test_create_task(tasks_book):
    """ Entry must be created to pass the test """
    result = tasks_book.add_task("make-a-snowman", "2024-12-25")
    assert result is not None


def test_delete_task(tasks_book):
    """ Ony entry must be deleted to pass the test """
    populated_storage(tasks_book)
    result = tasks_book.delete_task("make-a-snowman")

    assert result is not None
    assert result is not False


def test_set_completed_task(tasks_book):
    """ At least one entry must be edited to pass the test """
    populated_storage(tasks_book)
    result = tasks_book.complete_task("make-a-snowman")

    assert result is not None
    assert result is not False


def test_get_all_tasks(tasks_book):
    """ At least one entry must be present to pass the test """
    populated_storage(tasks_book)
    result = tasks_book.list_tasks()

    assert result is not None
    assert len(result) is not 0
