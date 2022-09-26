import re

def lambda_handler(event, context):
    print('Inside SAM!')
    lines = event['body'].splitlines()
    german_nos = {parse_german_no(line) for line in lines}
    return {
        'statusCode': 200,
        'body': list(german_nos)
    }

def _normalize_digits_only(number:str) -> str:
    """Normalizes a string of characters representing a phone number.
    Arguments:
    number -- a string representing a phone number
    Returns the normalized string version of the phone number.
    """
    number = number.strip()
    if len(number)<14: return None
    plus_prefix = "+" if number.startswith("+") else ""
    normalized_digits = ""
    for char_ in number:
        isdigit = char_.isdigit()
        if isdigit:
            normalized_digits += char_
        else:
            continue
    return plus_prefix + normalized_digits


def parse_german_no(line):
    telephone_no = _normalize_digits_only(line)
    if telephone_no and _is_german(telephone_no):
        return telephone_no


def _is_german(telephone_no: str) -> bool:
    p1 = re.compile('^0049\d{11}$')
    p2 = re.compile('^\+49\d{11}$')

    return p1.match(telephone_no) or p2.match(telephone_no)