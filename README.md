# FastAPI To-Do API

This is a simple To-Do API built using the FastAPI framework. The API allows users to create, read, update, and delete to-do items stored in a PostgreSQL database and a Redis cache. It also utilizes token-based authentication using JWT.

## Requirements

- PostgreSQL (version 9.5 or higher)
- Redis (version 3.2 or higher)
- Docker (version 19.03 or higher)
## Installation

Clone this repository.
```
git clone ...
```

## Running into a virtual env
Create and activate a virtual env
```
python -m venv venv
```
Activate the virtual env by running the following command
```
source myenv/bin/activate
```
check your terminal show (venv) before dir name
Install the required dependencies by running pip install -r requirements.txt.
Copy the .env.example file and rename it to .env.
Fill in the required environment variables in the .env file, including your PostgreSQL and Redis connection details.
In the file .env to create SECRET KEY using Linux or Macos run the command
```
openssl rand -hex 32
```
then set the key in the env file.
Start the application by running 
```
uvicorn app.main:app --reload
```
Before running the application, you can check the connection to PostgreSQL and Redis by running tests to ensure that the required services are available.

## Running into docker
Copy the `.env.db.example` file and rename it to `.env.db`
Copy the `.env.prod.example` file and rename it to `.env.prod`

In the file `.env.prod` to create SECRET KEY using Linux or Macos run the command
```
openssl rand -hex 32
```
then set the key in the env file.
Create the docker image by running the following command on root folde
```
docker build -t todo-fastapi . 
```
This is going to create a docker image named todo-fastapi.
Then start the application by running 
```
docker-compose -f docker-compose.yml up -d --build
```
This process may take a few minutes, depending on your network.

## Usage

Once the application is running, you can access the API documentation by visiting http://localhost:8000/docs.

To use the API, you will need to authenticate, so login with your username/email and password or create a new user

## Testing

To run the unit tests, with the virtual enviroment activated, run `pytest` in the root directory of the project. The tests are located in the tests/ directory.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or a pull request.

## Code Style

All code in this project follows the PEP8 style guide.

## Documentation

All code in this project is properly documented.