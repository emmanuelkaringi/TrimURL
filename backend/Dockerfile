#Specify the python image
FROM python:3.10.14-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY pyproject.toml poetry.lock ./

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Set PYTHONPATH
ENV PYTHONPATH=/app

# Copy the current directory contents into the container at /app
COPY . .

# Expose port 8000 for the app
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]