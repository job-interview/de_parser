import os
import boto3
from moto import mock_dynamodb
from DEParser.ddb import NumberProcessor

TABLE_NAME = 'DENumbers'
class MockNumberProcessor(NumberProcessor):
    def __init__(self) -> None:
        super().__init__()
        self.__aws_credentials()

    def __aws_credentials(self):
        """Mocked AWS Credentials for moto."""
        os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
        os.environ['AWS_SECURITY_TOKEN'] = 'testing'
        os.environ['AWS_SESSION_TOKEN'] = 'testing'
        os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
    
    @mock_dynamodb
    def _get_table_client(self):
        dynamodb = boto3.resource("dynamodb")
        params = {
            'TableName': 'DENumbers',
            'KeySchema': [
                {'AttributeName': 'PK', 'KeyType': 'HASH'},
                {'AttributeName': 'SK', 'KeyType': 'RANGE'}
            ],
            'AttributeDefinitions': [
                {'AttributeName': 'PK', 'AttributeType': 'S'},
                {'AttributeName': 'SK', 'AttributeType': 'S'}
            ],
            'BillingMode': 'PAY_PER_REQUEST'
        }
        table = dynamodb.create_table(**params)
        table.wait_until_exists()
        return table