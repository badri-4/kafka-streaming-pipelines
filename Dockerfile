FROM python:3.8-slim

WORKDIR /app

COPY consumer.py /app/consumer.py
COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

CMD ["python", "consumer.py"]
