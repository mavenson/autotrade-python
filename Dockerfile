# Dockerfile

FROM python:3.11-slim

# Set workdir
WORKDIR /app

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# This CMD will be overridden by docker-compose service commands
CMD ["python", "main.py"]
