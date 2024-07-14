# Tasks Book

## Description
A command line tool that lets you manage tasks and deadlines. the app lets you create, list, delete and complete taks.
The app is directly usable via compose, you only need to clone this repo and run given commands.

A logging system is implemented to keep track of launched commands and unexpected runtime errors, by default located in 
/var/log/tasksapp/logs.

## Configuration
The app is ready to work without further configuration. you can still edit some variables in docker-compose.yml:
- Windows users might have to change docker-compose logs location
- You can set MONGO_URI to a different database
- It is recommended to edit mongo default user and password

## Usage
#### Add a new task:
> docker compose run tasks_book --add-task "make-a-snowman" --due-date "2024-12-31"

#### Mark a task as completed:
> docker compose run tasks_book --complete-task "make-a-snowman"

#### List all tasks
> docker compose run tasks_book --list-tasks

#### Delete a task
> docker compose run tasks_book --delete-task make-a-snowman

You can also run the app as a module (without docker), makes sure to first install the requirements 
and set MONGO_URI env variable:

> MONGO_URI='mongodb://test_usr:test_pwd@localhost:27017/' python3 -m app --add-task "make-a-pumpkin" --due-date "2024-12-31"
## Testing
Unit testing using pytest is implemented to test all functionalities. 
it is required to either have the docker-compose mongo db running or set environment variables for 
MONGO_TEST_URI and MONGO_TEST_DB

Example:
> MONGO_TEST_URI='mongodb://test_usr:test_pwd@localhost:27017/' MONGO_TEST_DB='task_db_test' pytest

## Actions
A simple github actions is implemented to run unit tests on each push