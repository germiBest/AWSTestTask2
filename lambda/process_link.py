from urllib.parse import urlparse
import boto3
import uuid
import json
from datetime import datetime
import os
import feedparser
import socket

client = boto3.client('stepfunctions')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])
socket.setdefaulttimeout(1)


def link_processing(url):
    link = urlparse(url)
    try:
        if link.hostname in ("twitter.com", "twttr.com"):
            return("Twitter")
        elif len(feedparser.parse(url).entries) != 0:
            return("RSS")
        else:
            return("Website")
    except socket.timeout:
        return ("Website")

def lambda_handler(event, context):
    try:
        links = list(event["links"])
    except TypeError:
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
            stateMachineArn=os.environ["STATE_MACHINE"],
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
        try:
            item['callback'] = callback
        except KeyError:
            pass
        table.put_item(Item=item)
        resp.append(jobId)

    return {"idList": resp}

