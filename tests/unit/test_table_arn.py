from tests.unit.mock_number_processor import MockNumberProcessor

def test_table_arn():
    mock_number_processor = MockNumberProcessor()
    table = mock_number_processor._get_table_client()
    assert table.table_arn=='arn:aws:dynamodb:us-east-1:123456789012:table/DENumbers'