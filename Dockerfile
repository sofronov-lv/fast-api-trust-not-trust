FROM python:3.11-alpine

RUN mkdir /fastapi_trust_not_trust

WORKDIR /fastapi_trust_not_trust

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD alembic upgrade head && gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000