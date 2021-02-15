import requests
import os
from urllib.parse import urlparse


def process_twitter(message, context):
    response = {}
    try:
        response["Callback"] = message["Callback"]
    except:
        pass
    response["JobId"] = message["JobId"]
    response["Link"] = message["Link"]
    response["timestamp"] = message["timestamp"]
    
    link = urlparse(message["Link"])
    try:
        username = link.path.split('/')[1]
    except IndexError as e:
        print(e)
        response["Error"] = "Link is invalid"
        return (response)

    url = "https://api.twitter.com/2/users/by/username/" + username

    headers = {
        'Authorization':
        'Bearer ' + os.environ['bearerToken']
    }

    req_response = requests.request("GET", url, headers=headers)

    try:
        twitter_id = req_response.json()["data"]["id"]
    except KeyError:
        response["Error"] = "User is not found"
        return (response)

    url = "https://api.twitter.com/2/users/{}/tweets?max_results=5".format(
        twitter_id)

    try:
        req_response = requests.request("GET", url, headers=headers)

        resp_twttr = req_response.json()
        if resp_twttr["meta"]["result_count"] != 0 and "data" in resp_twttr:
            
            response["Result"] = resp_twttr["data"]
        else:
            response["Result"] = []
    except (KeyError, requests.exceptions.RequestException) as e:
        print(e)
        response["Error"] = "Request error"
    
    return (response)

