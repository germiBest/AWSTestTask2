from urllib.parse import urlparse
import boto3
import uuid
import json
from datetime import datetime

client = boto3.client('stepfunctions')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Test2API')

def link_processing(url):
    link = urlparse(url)
    if link.hostname in ("twitter.com", "twttr.com"):
        return("Twitter")
    elif link.path[-4:] in (".xml", ".rss"):
        return("RSS")
    else:
        return("Website")

def lambda_handler(event, context):
    # INPUT -> { "JobId": "uuid", "Callback": "url", "Link": "url"}
    try:
        links = list(event["links"])
    except TypeError as e:
        return {
            'Error': "Links is not provided"
        }
    
    if "callback" in event:
        callback = event["callback"]

    resp = []
    
    for link in links:
        jobId = str(uuid.uuid1())
        
        input = {}
        
        input["JobId"] = jobId
        try:
            input["Callback"] = callback
        except:
            pass
        input["Link"] = link
        input["LinkType"] = link_processing(link)
        input["timestamp"] = int(datetime.now().timestamp())
        client.start_execution(
            stateMachineArn='arn:aws:states:us-east-2:938668680897:stateMachine:Test2API_StateMachine',
            name=jobId,
            input=json.dumps(input)
        )
        item = {
                    'job_id': jobId,
                    'timestamp': input["timestamp"],
                    'link': link,
                    'state': 'Processing',
                    'linkType': input["LinkType"]
                }
        if 'callback' in locals():
            item['callback'] = callback
        table.put_item(Item=item)
        resp.append(jobId)

    return {"idList": resp}
