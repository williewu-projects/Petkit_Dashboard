# Use official Python base image (adjust tag to your Python version)
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=America/Los_Angeles

# Install system dependencies


# Set working directory inside the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app source code
COPY . /app/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Ensure the output directory exists
RUN mkdir -p static

EXPOSE 5000

# Run the graph generator script by default (you can override this at runtime)
CMD ["python", "flask_app.py"]
