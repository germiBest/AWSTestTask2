import time
import requests
import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

def result_processing(message, context):
    if "Error" in message:
        stte = "Error"
        res = message["Error"]
    else:
        stte = "Success"
        res = message["Result"]
        
    table.update_item(
        Key={
            'job_id': message["JobId"]
            #'timestamp': message["timestamp"]
        },
        UpdateExpression='SET #stte = :val1, #rslt = :result, #tmstmp = :tmstmp',
        ExpressionAttributeValues={
            ':val1': stte,
            ':result': str(res),
            ':tmstmp': int(message["timestamp"])
        },
        ExpressionAttributeNames={
          "#stte": "state",
          "#rslt": "result",
          "#tmstmp": "timestamp"
        }
    )
    data = {}
    try:
        if "Error" in message:
            data['Error'] = message["Error"]
        else:
            data['Result'] = message["Result"]
        requests.post(message["Callback"], data=json.dumps(data), headers={'Content-Type': 'application/json'})
    except requests.exceptions.RequestException:
        return({"Error": "CallbackEr"})
    except KeyError:
        return({})
