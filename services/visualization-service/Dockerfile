FROM python:3.12-slim
WORKDIR /app
COPY docker/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY shared /app/shared
COPY services/visualization-service /app/service
ENV PYTHONPATH=/app
CMD ["uvicorn", "service.main:app", "--host", "0.0.0.0", "--port", "8000"]
