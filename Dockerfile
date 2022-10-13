FROM python:3.9-slim-buster
# setting working directory
WORKDIR /app
# install aws sam cli and aws cli
RUN pip install aws-sam-cli==1.57.0 && pip install awscli==1.25.85