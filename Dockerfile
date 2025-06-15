# Use official Python base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY app/ ./app/

# Set environment variable for Python
ENV PYTHONUNBUFFERED=1

# Command to run your app (adjust as needed)
CMD ["python", "app/main.py"]

