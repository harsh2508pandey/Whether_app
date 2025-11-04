# Dockerfile
FROM python:3.11-slim

# Avoid buffering output (helps with logs)
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy only necessary files for faster caching
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port
EXPOSE 5000

# Use env var for production; default to 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--workers", "2", "--timeout", "60"]

