# Use the official Python 3.11 image as a base
FROM python:3.11-slim

# Install Poetry
RUN pip install poetry -i https://pypi.org/simple

# Set the working directory in the container
WORKDIR /app

# Copy only pyproject.toml and poetry.lock to leverage Docker cache
COPY pyproject.toml poetry.lock /app/

# Install dependencies without creating a virtual environment
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the remaining application files
COPY . /app

# Expose the port where FastAPI will run
EXPOSE 8000

# Command to run FastAPI (using Uvicorn server)
CMD alembic upgrade head && \
   gunicorn "app.main:get_application()" --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0 --timeout 600
