# Fast API boilerplate with JSON logger formatter
This is a boilerplate for a Fast API project with a JSON logger formatter.</br>
The purpose of this project is to provide a simple and fast way to start a new project with a JSON logger formatter.

## Medium article
This project is an example of the article [Python Logging: A Guide for Creating Informative Logs]()



## Pre-requisites
- Python 3.10
- Poetry (package manager) - https://python-poetry.org/docs/
- Docker (optional) - https://docs.docker.com/get-docker/

## Run the project locally (without Docker)
1. Clone the repository
2. Install the dependencies
```bash
poetry install
```
3. Run the project
```bash
poetry run gunicorn app.main:app --reload -c app/gunicorn_config.py
```

## Run with Docker
1. Build the image
```bash
docker build -t fastapi-boilerplate .
```
2. Run the container
```bash
docker run -p 8000:8000 fastapi-boilerplate
```
