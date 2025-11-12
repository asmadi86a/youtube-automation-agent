FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create necessary directories
RUN mkdir -p videos shorts logs

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the agent
CMD ["python", "youtube_agent.py"]
