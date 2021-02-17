import time
import requests


def process_website(message, context):
    response = {}
    try:
        response["Callback"] = message["Callback"]
    except:
        pass
    response["JobId"] = message["JobId"]
    response["Link"] = message["Link"]
    response["timestamp"] = message["timestamp"]

    url = message["Link"]

    try:
        response["Result"] = requests.get(url).elapsed.total_seconds()
    except requests.exceptions.RequestException as e:
        print(e)
        response["Error"] = "Requesting error"

    return response

