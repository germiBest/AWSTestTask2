import boto3
import json
import os
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

def lambda_handler(event, context):
    scan_kwargs = {
        "FilterExpression": Key('linkType').eq('Website')
    }
    resp = table.scan(**scan_kwargs)
    records = []
    for item in resp['Items']:
        records.append(item)

    return {"websites": records}

