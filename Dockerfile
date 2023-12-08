FROM python:3.7.2-alpine3.9

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "fetchServers.py"]



