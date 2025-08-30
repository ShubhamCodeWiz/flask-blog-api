# Dockerfile

FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy our new entrypoint script and the rest of the app code
COPY entrypoint.sh .
COPY . .

EXPOSE 8000

# NEW: The command to run is now our script
CMD ["./entrypoint.sh"]