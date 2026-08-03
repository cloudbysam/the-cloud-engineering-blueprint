# Stage 1: The Builder Stage
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a standalone virtual environment for our packages
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# Stage 2: The Final Production Runtime Stage
FROM python:3.11-slim

WORKDIR /app

# Copy the entire, fully compiled virtual environment over
COPY --from=builder /opt/venv /opt/venv
COPY app.py .

# Make sure the container runs everything using our virtual environment paths
ENV PATH="/opt/venv/bin:$PATH"
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["python", "app.py"]