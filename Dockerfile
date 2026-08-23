FROM docker.arvancloud.ir/python:3.12.0-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=core.settings.dev

WORKDIR /app

# Configure apt mirror
RUN rm -f /etc/apt/sources.list && \
    echo "deb http://mirror.mobinhost.com/debian/ bullseye main contrib non-free" > /etc/apt/sources.list && \
    echo "deb http://mirror.mobinhost.com/debian/ bullseye-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://mirror.mobinhost.com/debian-security bullseye-security main contrib non-free" >> /etc/apt/sources.list

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the ENTIRE project
COPY . /app/

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser /app
USER appuser

EXPOSE 8000
