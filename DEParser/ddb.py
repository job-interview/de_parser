import os
import re
import json
import boto3
import logging
import decimal
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

MINIMUM_LINE_LENGTH = 14
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
# create formatter and add it to the handler
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
# add the handler to the logger
logger.addHandler(handler)


class NumberProcessor:
    def __init__(self) -> None:
        self.is_local = bool(os.environ.get("AWS_SAM_LOCAL"))

    def process(self, job_id, lines):
        german_nos = list({self._parse_german_no(line) for line in lines})
        job_id = self._put_results(job_id, german_nos)
        self._update_job_list(job_id)
        return job_id
    def get_results(self, job_id):
        table = self._get_table_client()
        try:
            data = table.get_item(Key={"PK":"job_id", "SK": job_id})
            if not data.get("Item"):
                raise KeyError

        except ClientError as e:
            logger.exception("DynamoDB Client Error!")
            raise e
        except KeyError as e:
            logger.warning(
                "Job not found at DB! JobId: {JobId}".format(JobId=job_id)
            )
            return None
        return data.get("Item")
    
    def list_jobs(self):
        table = self._get_table_client()
        try:
            data = table.query( KeyConditionExpression=Key('PK').eq('job'))
            if not data.get("Items"):
                raise KeyError

        except ClientError as e:
            logger.exception("DynamoDB Client Error!")
            raise e
        except KeyError as e:
            logger.warning(
                "PK:job not found at DB!"
            )
            return None

        items =  data.get("Items")
        job_ids = [item['SK'] for item in items]
        return job_ids
    
    def delete_results(self, job_id):
        table = self._get_table_client()
        try:
            data = table.delete_item(Key={"PK":"job_id", "SK": job_id})
            if not data.get("Item"):
                raise KeyError

        except ClientError as e:
            logger.exception("DynamoDB Client Error!")
            raise e
        except KeyError as e:
            logger.warning(
                "Job not found at DB! JobId: {JobId}".format(JobId=job_id)
            )
            return None
        job_id = self._remove_job_list(job_id=job_id)

        return job_id

    def _put_results(self, job_id, numbers):
        table = self._get_table_client()
        try:
            table.put_item(
                Item={"PK": "job_id", "SK": job_id, "numbers": numbers},
                ConditionExpression="attribute_not_exists(PK)",
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                logger.exception(
                    "Job already exists! job_id: {job_id}".format(job_id=job_id)
                )
                raise e
            logger.exception("DynamoDB Client Error!")
            raise e
        else:
            logger.warning("Numbers saved! JobId: {job_id}".format(job_id=job_id))
            return job_id

    def _update_job_list(self, job_id):
        table = self._get_table_client()
        try:
            table.put_item(Item={"PK": "job", "SK": job_id})
        except ClientError as e:
            logger.exception("DynamoDB Client Error!")
            raise e
        else:
            logger.warning(
                "JobId: {job_id} added to the processed jobs list".format(job_id=job_id)
            )
            return job_id
    
    def _remove_job_list(self, job_id):
        table = self._get_table_client()
        try:
            table.delete_item(Item={"PK": "job", "SK": job_id})
        except ClientError as e:
            logger.exception("DynamoDB Client Error!")
            raise e
        else:
            logger.warning(
                "JobId: {job_id} removed from processed jobs list".format(job_id=job_id)
            )
            return job_id

    def _get_table_client(self):
        table_name = os.environ.get("TABLE_NAME")
        endpoint_url = os.environ.get("DDB_ENDPOINT_URL")
        if self.is_local:
            dynamodb = boto3.resource("dynamodb", endpoint_url=endpoint_url)
        else:
            dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(table_name)
        return table

    @staticmethod
    def _normalize_digits_only(number: str) -> str:
        """Normalizes a string of characters representing a phone number.
        Arguments:
        number -- a string representing a phone number
        Returns the normalized string version of the phone number.
        """
        number = number.strip()
        if len(number) < MINIMUM_LINE_LENGTH:
            return None
        plus_prefix = "+" if number.startswith("+") else ""
        char_list = [char_ for char_ in number if char_.isdigit()]
        normalized_digits = "".join(char_list)
        return plus_prefix + normalized_digits

    def _parse_german_no(self, line):
        telephone_no = self._normalize_digits_only(line)
        if telephone_no and self._is_german(telephone_no):
            return telephone_no

    @staticmethod
    def _is_german(telephone_no: str) -> bool:
        p1 = re.compile("^0049\d{11}$")
        p2 = re.compile("^\+49\d{11}$")

        return p1.match(telephone_no) or p2.match(telephone_no)

    @staticmethod
    def _response(response, is_local=False):
        print("IS_LOCAL: ", is_local)
        if is_local:
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Content-Type": "application/json",
                },
                "body": json.dumps(response),
            }
        return {
            "statusCode": 200,
            "body": json.dumps(response),
            "headers": {"Content-Type": "application/json"},
        }


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)