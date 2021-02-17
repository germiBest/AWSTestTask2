# AWSTestTask2
 Second test task of AWS service development
# Deploy
Setup the ``bearerToken`` in ``serverless.yaml``

Localy install python dependencies (in case serverless-python-requirements doesn't working :( )
```shell
pip install -r requirements.txt -t .
serverless plugin install --name serverless-step-functions
```

```shell
serverless deploy
```

# API
 Documentation is provided [here](http://avia.bid/swagger.html).

 Example of ``data`` for /jobs POST
 ```json
{
   "links":[
      "https://twitter.com/elonmusk",
      "http://avia.bid/rss2_example_perfsys.xml",
      "https://google.com"
   ],
   "callback":"https://callback.com/callbackurl123"
}
 ```