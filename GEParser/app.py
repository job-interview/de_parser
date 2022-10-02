import json
from ddb import NumberProcessor

MINIMUM_LINE_LENGTH=14

def lambda_handler(event, context):
    job_id = context.aws_request_id
    lines = event['body'].splitlines()
    number_processor = NumberProcessor()
    job_id =  number_processor.process(job_id, lines)
    return {
        'statusCode': 200,
        'body': json.dumps({'job_id':job_id})
    }

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


def _parse_german_no(line):
    telephone_no = _normalize_digits_only(line)
    if telephone_no and _is_german(telephone_no):
        return telephone_no


def _is_german(telephone_no: str) -> bool:
    import re
    p1 = re.compile('^0049\d{11}$')
    p2 = re.compile('^\+49\d{11}$')

    return p1.match(telephone_no) or p2.match(telephone_no)