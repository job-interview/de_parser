import os
import re
import json
import boto3
import logging
import decimal
from botocore.exceptions import ClientError

MINIMUM_LINE_LENGTH = 14
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
# create formatter and add it to the handler
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
# add the handler to the logger
logger.addHandler(handler)

class NumberProcessor:
    def process(self, job_id, lines):
        german_nos = list({self._parse_german_no(line) for line in lines})
        job_id = self._put_record(job_id, german_nos)
        return job_id
    def _put_record(self, job_id, numbers):
        table = self._get_table_client()
        try:
            table.put_item(
                Item={"PK": "job_id","SK":job_id, "numbers":numbers },
                ConditionExpression="attribute_not_exists(PK)",
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                logger.exception(
                    "Job already exists! job_id: {job_id}".format(
                        job_id=job_id
                    )
                )
                raise e
            logger.exception("DynamoDB Client Error!")
            raise e
        else:
            logger.warning("Numbers saved! JobId: {job_id}".format(job_id=job_id))
            return job_id
    def _get_table_client(self):
        is_local = os.environ.get('AWS_SAM_LOCAL')
        table_name = os.environ.get('TABLE_NAME')
        endpoint_url = os.environ.get('DDB_ENDPOINT_URL')
        if is_local:
            dynamodb = boto3.resource("dynamodb", endpoint_url=endpoint_url)
        else:
            dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(table_name)
        return table
    @staticmethod
    def _normalize_digits_only(number:str) -> str:
        """Normalizes a string of characters representing a phone number.
        Arguments:
        number -- a string representing a phone number
        Returns the normalized string version of the phone number.
        """
        number = number.strip()
        if len(number)<MINIMUM_LINE_LENGTH: return None
        plus_prefix = "+" if number.startswith("+") else ""
        char_list = [char_ for char_ in number if char_.isdigit()]
        normalized_digits = ''.join(char_list)
        return plus_prefix + normalized_digits


    def _parse_german_no(self, line):
        telephone_no = self._normalize_digits_only(line)
        if telephone_no and self._is_german(telephone_no):
            return telephone_no

    @staticmethod
    def _is_german(telephone_no: str) -> bool:
        p1 = re.compile('^0049\d{11}$')
        p2 = re.compile('^\+49\d{11}$')

        return p1.match(telephone_no) or p2.match(telephone_no)



# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)