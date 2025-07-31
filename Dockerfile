# Use Python 3.11 slim base image
FROM python:3.11-slim

# Prevent interactive prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# Install build-essential for compiling any dependencies if needed
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Environment settings
ENV PYTHONUNBUFFERED=1

# Run the main app
CMD ["python", "main.py"]
