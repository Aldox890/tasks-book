FROM python:3.11-slim

Workdir /code
RUN mkdir ./logs && touch ./logs/task_book.log
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python3", "-m", "app"]