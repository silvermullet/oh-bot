#!/bin/bash

if [ -e localdev/DynamoDBLocal.jar ]; then
	echo "DynamoDB local is already in place..."
	ls localdev/
else
	echo "Downloading DynamoDB local..."
	wget https://s3-us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.tar.gz -O ./localdev/dynamodb_local_latest.tar.gz
	pushd ./localdev
	tar -xvf dynamodb_local_latest.tar.gz
	popd
fi
