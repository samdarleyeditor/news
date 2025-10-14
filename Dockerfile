# Use official Python image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Python code
COPY main.py main.py

# Expose port (Cloud Run expects app listens on $PORT)
ENV PORT 8080
EXPOSE 8080

# Run the app with Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
