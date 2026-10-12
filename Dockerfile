FROM python:3.11-slim

# Install system dependencies including Git and Node.js for Jest
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    nodejs \
    npm \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency specifications
COPY requirements.txt package.json ./

# Install Python and Node dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    npm install --omit=optional

# Copy application source
COPY . .

# Configure Git defaults
RUN git config --global user.name "IBM Bob Agent" && \
    git config --global user.email "bob@ibm.com"

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
