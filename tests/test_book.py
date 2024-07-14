import os
import pytest

from pymongo import MongoClient
from app.task_book import TaskBook

mongo_test_uri = os.getenv('MONGO_TEST_URI', 'mongodb://test_usr:test_pwd@localhost:27017/')
mongo_test_db = os.getenv('MONGO_TEST_DB', 'task_db_test')


@pytest.fixture(scope="module")
def mongo_client():
    """ Yields a connection to the database """
    client = MongoClient(mongo_test_uri)
    yield client
    client.close()


@pytest.fixture(scope="module")
def clean_db(mongo_client):
    """ Ensure to clear the database before every unit test """
    db = mongo_client[mongo_test_db]
    db.drop_collection('task')


@pytest.fixture(scope="module", autouse=True)
def populated_storage(clean_db):
    """
    Populate the database for testing
    Ensures to run a newly populated database for each unit test
    """
    tasks_book = TaskBook(mongo_test_uri, mongo_test_db)
    tasks_book.add_task("make-a-snowman", "2024-12-25")
    tasks_book.add_task("make-a-drink", "2024-12-31")
    tasks_book.add_task("make-a-firework", "2025-1-29")

    return tasks_book


def test_create_task(populated_storage):
    """ Entry must be created and unique to pass the test """

    # Entry can be added
    result = populated_storage.add_task("make-a-pumpkin", "2024-10-31")
    if result is None:
        assert False

    # Entry cannot must not be duplicated
    result = populated_storage.add_task("make-a-pumpkin", "2024-10-31")
    assert result is None


def test_set_completed_task(populated_storage):
    """ At least one entry must be edited to pass the test """
    result = populated_storage.complete_task("make-a-snowman")

    assert result is not None
    assert result is not False


def test_delete_task(populated_storage):
    """ Ony entry must be deleted to pass the test """
    result = populated_storage.delete_task("make-a-snowman")

    assert result is not None
    assert result is not False


def test_get_all_tasks(populated_storage):
    """ At least one entry must be present to pass the test """
    result = populated_storage.list_tasks()

    assert result is not None
    assert len(result) != 0
