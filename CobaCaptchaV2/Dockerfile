FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install Firefox & dependencies
RUN apt-get update && apt-get install -y \
    firefox-esr \
    ca-certificates \
    wget \
    gnupg \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app

# Create non-root user
RUN useradd --create-home appuser
USER appuser
ENV HOME=/home/appuser

# Run the script
CMD ["python", "Firefox.py"]
