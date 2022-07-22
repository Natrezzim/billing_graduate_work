FROM python:3.9-slim-buster

RUN apt-get update -y && apt-get upgrade -y && apt-get install iputils-ping -y

WORKDIR /billing

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]