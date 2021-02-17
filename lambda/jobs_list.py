import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

def lambda_handler(event, context):
    resp = table.scan()
    records = []
    for item in resp['Items']:
        records.append(item)

    return {"jobs": records}
import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

def lambda_handler(event, context):
    resp = table.scan()
    records = []
    for item in resp['Items']:
        records.append(item)

    return {"jobs": records}

