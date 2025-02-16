FROM mcr.microsoft.com/devcontainers/python:3.10

# Install necessary packages
RUN apt-get update && apt-get install -y \
    wget \
    software-properties-common \
    ssh \
    && rm -rf /var/lib/apt/lists/*

# Create workspace directory
WORKDIR /workspace

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt