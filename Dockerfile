FROM python:3.11-slim

WORKDIR /app
COPY app/ /app/

RUN apt-get update && apt-get install -y gcc default-libmysqlclient-dev \
    && pip install --no-cache-dir -r requirements.txt

ENV PORT=8080
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
