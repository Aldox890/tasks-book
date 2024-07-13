import argparse
import logging
import os
from datetime import datetime

from app.data_models import Task
from app.task_storage import TaskStorage


class TaskBook:

    def __init__(self, mongo_uri, task_db):
        self.storage = TaskStorage(mongo_uri, task_db)

    def add_task(self, task_description, due_date):
        """ Add a task new task to the tasks book with its deadline """
        try:
            format_datetime = datetime.strptime(due_date, '%Y-%m-%d')
            new_task = Task(task_description=task_description, due_date=format_datetime)
            result = self.storage.create_task(new_task)
        except ValueError as e:
            print(e)
            return None
        except Exception as e:
            print(e)
            return None

        print(f"Task {task_description} with due date {due_date} created successfully")
        return result

    def list_tasks(self):  # TODO
        """ List all available tasks with their deadline and status"""
        result = self.storage.get_all_tasks()

        print("Booked tasks:\n")
        for task in self.storage.get_all_tasks():
            print(f"{task.task_description} - {task.due_date} - {task.is_completed}\n")

        return result

    def complete_task(self, task_description):  # TODO
        """ Mark a task as completed """
        result = self.storage.set_task_completed(task_description)
        return result

    def delete_task(self, task_description):  # TODO
        """ Removes a task from the book """
        result = self.storage.delete_task(task_description)
        return result

    def close_book(self):
        self.storage.close_storage()


def parse_task():
    parser = argparse.ArgumentParser(description="Tasks Book - helps you keep your deadlines!")
    parser.add_argument("--add-task", metavar="[task description]", help="Add a new task, due date is required")
    parser.add_argument("--due-date", metavar="[YYYY-MM-DD]", help="Set task due date")
    parser.add_argument("--list-tasks", action='store_true', help="Display all tasks")
    parser.add_argument("--complete-task", metavar="[task description]", help="Mark a task as complete")
    parser.add_argument("--delete-task", metavar="[task description]", help="Delete a task from the book")
    args = parser.parse_args()

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

    task_book.close_book()


if __name__ == "__main__":
    parse_task()
