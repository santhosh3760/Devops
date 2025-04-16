FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Remove any existing log files (they shouldn't be in the container)
RUN rm -f app.log*

# Create directories for flask-session if they don't exist
RUN mkdir -p flask_session

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 8000

# Use Gunicorn as the production server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]