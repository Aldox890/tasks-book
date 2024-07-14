"""
    Main script for the module, implements the user interface for the app

    Classes
    ---------
    TasksBook(mongo_uri, task_db): implements all functions the user requires to interact with the tasks book
    ---------

    Functions
    ---------
    parse_task(): main entrypoint for the app, parses and interprets the user input
    setup_logger(): returns configured logger file
    ---------

"""
import argparse
import os
import logging

from datetime import datetime

from app.data_models import Task
from app.task_storage import TaskStorage


class TaskBook:
    """
    Class used as user interface for the tasks book

    Methods
    ---------
    add_task(task_description, due_date): add a new task to the book, task description must be unique
    list_tasks(): list all available tasks
    complete_task(): mark task_description as completed
    delete_task(): delete task_description from book
    close_book(): terminates database connection
    ---------
    """
    def __init__(self, mongo_uri, task_db):
        self.storage = TaskStorage(mongo_uri, task_db)

    def add_task(self, task_description, due_date):
        """ Add a task new task to the tasks book with its deadline """
        try:
            format_datetime = datetime.strptime(due_date, '%Y-%m-%d')
            present = datetime.now()

            # Check that due date is before current date
            if format_datetime.date() < present.date():
                print("Due date cannot be prior today's date")
                return None

            new_task = Task(task_description=task_description, due_date=format_datetime)
            result = self.storage.create_task(new_task)

            print(f"Task {task_description} with due date {due_date} created successfully")
        except ValueError as e:
            print(e)
            return None
        return result

    def list_tasks(self):
        """ List all available tasks with their deadline and status"""
        result = self.storage.get_all_tasks()

        if len(result) == 0:
            print("Tasks book is empty.")
        else:
            # Print all tasks
            print("Stored tasks: ")
            for task in self.storage.get_all_tasks():
                print(f"Task: {task.task_description} - "
                      f"Due date: {task.due_date.date()} - "
                      f"Completed: {task.is_completed}")

        return result

    def complete_task(self, task_description):
        """ Mark a task as completed """
        result = self.storage.set_task_completed(task_description)

        if result is False:
            print(f"Task {task_description} not found")
        else:
            print(f"Task {task_description} updated successfully")
        return result

    def delete_task(self, task_description):
        """ Removes a task from the book """
        result = self.storage.delete_task(task_description)

        if result is False:
            print(f"Task {task_description} not found")
        else:
            print(f"Task {task_description} deleted successfully")

        return result

    def close_book(self):
        """ Close database connection """
        self.storage.close_storage()


def setup_loger():
    """ Setup logging configuration """
    logger = logging.getLogger(__name__)

    if not os.path.exists("./logs"):
        os.makedirs("./logs")

    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        filename='./logs/task_book.log',
                        level=logging.INFO)

    return logger


def parse_task():
    """ Parse arguments and call book functions """
    logger = setup_loger()
    parser = argparse.ArgumentParser(description="Tasks Book - helps you keep your deadlines!")

    parser.add_argument("-a", "--add-task", metavar="[task description]", help="Add a new task, due date is required")
    parser.add_argument("-d", "--due-date", metavar="[YYYY-MM-DD]", help="Set task due date")
    parser.add_argument("-l", "--list-tasks", action='store_true', help="Display all tasks")
    parser.add_argument("-c", "--complete-task", metavar="[task description]", help="Mark a task as complete")
    parser.add_argument("-r", "--delete-task", metavar="[task description]", help="Delete a task from the book")
    args = parser.parse_args()

    try:
        # keep track of all commands
        logger.info(args)

        # tasks book setup
        task_book = TaskBook(os.environ['MONGO_URI'], 'task_db')

        # Parse input action
        if args.add_task and args.due_date:
            task_book.add_task(args.add_task, args.due_date)
        elif args.list_tasks:
            task_book.list_tasks()
        elif args.complete_task:
            task_book.complete_task(args.complete_task)
        elif args.delete_task:
            task_book.delete_task(args.delete_task)
        else:
            print("Error: Invalid command. Use --help for usage information.")
    except Exception as e:
        # Log any unexpected error that might happen
        logger.error(e)
        return False

    task_book.close_book()
    return True


if __name__ == "__main__":
    parse_task()
