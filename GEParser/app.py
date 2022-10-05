import json
from ddb import NumberProcessor

MINIMUM_LINE_LENGTH = 14


def lambda_handler(event, context):
    if event["httpMethod"] == "GET" and event["resource"] == "/job":
        number_processor = NumberProcessor()
        results = number_processor.get_results(job_id)
        return number_processor._response(results, number_processor.is_local)
    if event["httpMethod"] == "DELETE" and event["resource"] == "/job":
        number_processor = NumberProcessor()
        job_id = number_processor.delete_results(job_id)
        return number_processor._response({"job_id": job_id}, number_processor.is_local)
    if event["httpMethod"] == "GET" and event["resource"] == "/jobs":
        number_processor = NumberProcessor()
        job_ids = number_processor.list_jobs()
        return number_processor._response({"job_ids": job_ids}, number_processor.is_local)
    if event["httpMethod"] == "POST" and event["resource"] == "/job":
        job_id = context.aws_request_id
        lines = event["body"].splitlines()
        number_processor = NumberProcessor()
        job_id = number_processor.process(job_id, lines)
        response = number_processor._response({"job_id": job_id}, number_processor.is_local)
        # print('Response: ', response)
        return response
