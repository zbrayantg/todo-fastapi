# FastAPI To-Do API

This is a simple To-Do API built using the FastAPI framework. The API allows users to create, read, update, and delete to-do items stored in a PostgreSQL database and a Redis cache. It also utilizes token-based authentication using JWT.

# Getting Started
Open your preferred web browser and go to the following address:
```
http://20.241.204.95/docs
```

This will open the Swagger UI documentation for the API, where you can explore and interact with the available endpoints.

To access protected endpoints, you will need to create a user account and obtain an access token.
Click on the "Create User" endpoint in the Swagger UI and provide the required information to create a new user

After successfully creating the user, use the user credentials to authenticate and obtain an access token.

Once you have the access token, you can use it to authorize your requests to protected endpoints.

Feel free to make CRUD operations on tasks using the provided endpoints.
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

## Local Usage

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

# Contact

For any questions or inquiries, please contact:

Brayant Gualdron (zbgualdron@gmail.com)
Feel free to reach out with any feedback or suggestions!