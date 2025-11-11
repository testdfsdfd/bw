# Base image with Python
FROM python:3.13-slim

# Install Firefox, Xvfb, and dependencies
RUN apt-get update && \
    apt-get install -y \
        firefox \
        wget \
        gnupg \
        libgtk-3-0 \
        libdbus-glib-1-2 \
        libdbus-1-3 \
        libxt6 \
        libx11-xcb1 \
        libdrm2 \
        libxcomposite1 \
        libxdamage1 \
        libxrandr2 \
        libasound2 \
        fonts-liberation \
        libnss3 \
        libnspr4 \
        xvfb \
        x11-utils \
        && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Command to start Xvfb and your Python script
CMD ["sh", "-c", "Xvfb :99 -screen 0 1920x1080x24 & export DISPLAY=:99 && python Firefox.py"]
