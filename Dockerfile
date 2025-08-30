# Dockerfile

# 1. Start from an official, lightweight Python base image
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file first to leverage Docker's layer caching
COPY requirements.txt .

# 4. Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code into the container
COPY . .

# 6. Expose the port Gunicorn will run on
EXPOSE 8000

# 7. Define the command to run your app using Gunicorn
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "wsgi:app"]