# Use Python 3.9 as the base image
FROM python:3.9

# Install the netcat package for checking database availability
RUN apt-get update && apt-get install -y netcat

# Set the working directory to /code
WORKDIR /code

# Copy the requirements file to /code/requirements.txt
COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip

# Install the required Python packages listed in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the application code from the host machine to /code/app in the container
COPY ./app /code/app

# Check the availability of the database before starting the application
# Wait until the database is available using netcat
# Once the database is available, start the application with uvicorn
CMD while ! nc -z $DB_HOST $DB_PORT; do sleep 0.1; done && uvicorn app.main:app --host 0.0.0.0 --port 80
