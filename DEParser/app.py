from ddb import NumberProcessor

MINIMUM_LINE_LENGTH = 14


def lambda_handler(event, context):
    operation_name = event["requestContext"]["operationName"]
    http_method = event["httpMethod"]
    if http_method == "GET" and operation_name == "getJobById":
        job_id = event['pathParameters']['job_id']
        number_processor = NumberProcessor()
        results = number_processor.get_results(job_id)
        return number_processor._response(results, number_processor.is_local)
    if http_method == "DELETE" and operation_name == "deleteJob":
        number_processor = NumberProcessor()
        job_id = number_processor.delete_results(job_id)
        return number_processor._response({"job_id": job_id}, number_processor.is_local)
    if event["httpMethod"] == "GET" and event["resource"] == "/jobs":
        number_processor = NumberProcessor()
        job_ids = number_processor.list_jobs()
        return number_processor._response({"job_ids": job_ids}, number_processor.is_local)
    if http_method == "POST" and operation_name == "addJob":
        job_id = context.aws_request_id
        lines = event["body"].splitlines()
        number_processor = NumberProcessor()
        job_id = number_processor.process(job_id, lines)
        response = number_processor._response({"job_id": job_id}, number_processor.is_local)
        return response
