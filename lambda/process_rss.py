import feedparser


def process_rss(message, context):
    response = {}
    try:
        response["Callback"] = message["Callback"]
    except KeyError:
        pass
    response["JobId"] = message["JobId"]
    response["Link"] = message["Link"]
    response["timestamp"] = message["timestamp"]

    link = message["Link"]
    try:
        NewsFeed = feedparser.parse(link)
        response["Result"] = NewsFeed.entries[0:5]
    except BaseException as e:
        response["Error"] = e
    return response

