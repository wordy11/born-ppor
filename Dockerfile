# Start with a Python image (you can choose your version)
FROM python:3.9-slim

# Install apturl and other system dependencies
RUN apt-get update && apt-get install -y apturl && apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (if applicable)
EXPOSE 8000

# Set the command to run your application (adjust as needed)
CMD ["python3", "app.py"]
