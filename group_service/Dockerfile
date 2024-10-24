FROM python:3.10-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

ENV PYTHONPATH=${PYTHONPATH}

RUN apt-get update \
    && apt-get install gcc libpq-dev -y \
    && apt-get clean

RUN pip install -r /app/requirements.txt \
&& rm -rf /root/.cache/pip
    
COPY . /app/