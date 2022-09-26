FROM python:3.9-slim-buster
WORKDIR /app
VOLUME /var/run/docker.sock
RUN apt update && apt upgrade -y
RUN pip install aws-sam-cli==1.57.0
