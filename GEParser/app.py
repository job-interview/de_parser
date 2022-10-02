import json
from ddb import NumberProcessor

MINIMUM_LINE_LENGTH=14


def lambda_handler(event, context):
    # if event["httpMethod"] == "GET":
    #     response = get_cause_details(event, context)
    #     return response
    if event["httpMethod"] == "POST":
        job_id = context.aws_request_id
        lines = event['body'].splitlines()
        number_processor = NumberProcessor()
        job_id =  number_processor.process(job_id, lines)
        return {
            'statusCode': 200,
            'body': json.dumps({'job_id':job_id})
        }
    # if event["httpMethod"] == "PUT":
    #     response = put_cause_details(event, context)
    #     return response