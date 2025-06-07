FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app/app
COPY tests /app/tests

CMD ["gunicorn", "app.main:app", "--bind", "0.0.0.0:80"] 