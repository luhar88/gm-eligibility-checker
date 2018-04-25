FROM python:3.6

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV PYTHONPATH=$PYTHONPATH:/usr/src/app

COPY . /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt
