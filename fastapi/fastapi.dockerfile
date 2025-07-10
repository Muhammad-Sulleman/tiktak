# fastapi/fastapi.dockerfile

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./api /app/api


# Run the app
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "4000"]
