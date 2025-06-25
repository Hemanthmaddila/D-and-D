FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements-minimal.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements-minimal.txt

# Copy all application files
COPY . .

# Set environment variables
ENV PYTHONPATH="/app"
ENV PYTHONUNBUFFERED=1

# Expose the port
EXPOSE 8080

# Start the application using the main.py entry point
CMD ["python", "main.py"] 