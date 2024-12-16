FROM python:3.11-alpine

RUN mkdir /fastapi_trust_not_trust

WORKDIR /fastapi_trust_not_trust

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
