import uuid
import json
from tests.unit.mock_number_processor import MockNumberProcessor
from moto import mock_dynamodb

@mock_dynamodb
def test_add_job():
    mock_number_processor = MockNumberProcessor()
    job_id = uuid.uuid1().__str__()
    event_add_job = json.load(open('events/addJob.json'))
    lines = event_add_job["body"].splitlines()
    ddb_job_id = mock_number_processor.process(job_id, lines)
    assert ddb_job_id==job_id
