FROM python:3.10-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests pkg-config build-essential default-libmysqlclient-dev

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 5000

CMD [ "python3", "server.py" ]