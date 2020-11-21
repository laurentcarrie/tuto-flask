FROM ubuntu:20.04

RUN adduser microblog

WORKDIR /home/microblog


RUN apt-get update
RUN apt-get install -y python
RUN apt-get install -y virtualenv
RUN apt-get install -y postgresql-client

COPY requirements.txt requirements.txt
RUN virtualenv venv --python=3.8
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY microblog.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP microblog.py

RUN chown -R microblog:microblog ./
USER microblog

EXPOSE 5000
