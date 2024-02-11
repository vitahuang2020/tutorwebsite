# Base Image
FROM python:3.9-slim

# Work directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt requirements.txt

# Install build-essential and other necessary development libraries
RUN apt-get update && \
    apt-get install -y build-essential libssl-dev libffi-dev python3-dev

RUN pip install -r requirements.txt

# Copy other project files
COPY . .

# Expose a port to Containers
EXPOSE 8080

# Set environment variables
ENV DATABASE_URL="your_database_url"

# Command to run on server
CMD ["gunicorn", "-b", "0.0.0.0:8080", "--reload", "app:app"]