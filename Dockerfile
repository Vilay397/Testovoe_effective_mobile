# Base: Python 3.10
FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system deps: Chromium & Chromedriver, Java (for Allure CLI), unzip, xvfb
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    default-jre \
    xvfb \
    xauth \
    wget \
    unzip \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Allure CLI
ARG ALLURE_VERSION=2.29.0
RUN wget -q https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.zip -O /tmp/allure.zip \
    && unzip /tmp/allure.zip -d /opt \
    && ln -s /opt/allure-${ALLURE_VERSION}/bin/allure /usr/bin/allure \
    && rm /tmp/allure.zip

# Workdir
WORKDIR /app

# Python dependencies
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Project files
COPY . .

# Allure server port
EXPOSE 8080

# Default to interactive shell
CMD ["bash"]
