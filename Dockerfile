# Python base image
FROM python:3.11-slim

# ✅ Install system packages for GUI (Tkinter) and X11 support
RUN apt-get update && apt-get install -y \
    # Tkinter GUI support  
    python3-tk \ 
    # X11 library to communicate with host display       
    libx11-6 \  
    # Clean up to keep image size small        
    && apt-get clean     # Clean up to keep image size small

# Set the working directory inside the container
WORKDIR /app

# ✅ Copy Python dependencies file and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY app/ ./app/

# Set environment variable for Python
ENV PYTHONUNBUFFERED=1

# Command to run your app
CMD ["python", "app/main.py"]

