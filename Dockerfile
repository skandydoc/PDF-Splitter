# Use the official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create Output Files directory
RUN mkdir -p "Output Files"

# Expose the port the app runs on
EXPOSE 8080

# Set the default port for Cloud Run
ENV PORT=8080

# Health check
HEALTHCHECK CMD curl --fail http://localhost:$PORT/_stcore/health

# Run the application
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --server.fileWatcherType=none 