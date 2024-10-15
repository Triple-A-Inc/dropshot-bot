# Use Python 3.8 as the base image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy the application files to the container
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Set the PYTHONPATH explicitly
ENV PYTHONPATH="/app/ai"

# Set the command to run the app with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "ai.app:app"]