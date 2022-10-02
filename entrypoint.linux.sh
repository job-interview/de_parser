aws dynamodb create-table --table-name GENumbers \
    --attribute-definitions AttributeName=job_id,AttributeType=S \
    --key-schema AttributeName=job_id,KeyType=HASH \
    --endpoint-url http://dynamodb-local:8000 \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
sam local start-api -p 3000 --host 0.0.0.0 --docker-network aws_backend --container-host 172.17.0.1 --container-host-interface 0.0.0.0