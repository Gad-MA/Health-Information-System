FROM python:3.11-slim

# Prevent Python from writing .pyc files and force stdout flush
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=backend.settings

# Set working directory
WORKDIR /app

# Install libpq and other needed system dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy your Django project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput || echo "collectstatic failed"

# Expose port 8000 for gunicorn
EXPOSE 8000

# Start Gunicorn server
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
