# Base Image
FROM python:3.12-slim

# Working directory inside the container
WORKDIR /app

# Copy dependency file first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project
COPY . .

# Flask port
EXPOSE 5000

# Start the application
CMD ["python", "run.py"]