aws dynamodb create-table --table-name DENumbers \
    --attribute-definitions AttributeName=PK,AttributeType=S AttributeName=SK,AttributeType=S \
    --key-schema AttributeName=PK,KeyType=HASH AttributeName=SK,KeyType=RANGE \
    --endpoint-url http://dynamodb-local:8000 \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
sam local start-api -p 3000 --host 0.0.0.0 --docker-network aws_backend \
    --container-host host.docker.internal \
    --container-env-vars ./.aws.json