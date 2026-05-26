# Use an official, lightweight Python runtime
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /code

# Copy requirements and install them
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the application source code
COPY ./app /code/app

# Expose the port FastAPI runs on
EXPOSE 8000

# Run the app via uvicorn when the container starts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]