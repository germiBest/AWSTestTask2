import json
import boto3
from boto3.dynamodb.conditions import Key
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

def lambda_handler(event, context):
    response = table.scan()
    answ = None
    temp_tstmp = 0
    for item in response["Items"]:
        if item["linkType"] == "Website" and event["domain"] in item["link"] and item["timestamp"] > temp_tstmp:
            temp_tstmp = item["timestamp"]
            answ = item
    return answ

