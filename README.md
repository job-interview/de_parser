## DEParser

A simple serverless api to parser German phone numbers

### Tech stack
- AWS Lambda
- AWS APIGateway
- AWS DynamoDB

### Run locally

To run it locally, following tool is requried
* Docker - [Install Docker](https://www.docker.com/products/docker-desktop/)

- Update the `docker-compose.yml` entrypoint at line 15 based on the operating system being and Run `docker compose up --build`
- visit `http://localhost:8001` for DynamoDB UI
- visit `http://localhost:8002` for SwaggerUI

### Run tests

Run `pytest tests/unit/` to run unit tests

### Test live

Live test endpoint: https://fwhqew31r3.execute-api.us-west-2.amazonaws.com/dev

### Deploy the application

The application can be deployed in AWS using AWS SAM CLI.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)

Run `sam deploy --guided` and follow the steps to deploy to AWS account.