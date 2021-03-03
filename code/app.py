import os
import json

def response(body={}, status_code=200):
    return {
        "statusCode": status_code,
        "body": json.dumps(body),
    }

def lambda_handler(event, context):
    print(os.environ)
    print(os.environ.get('Bucket','Not found bucket'))
    return response(
            {
                "message": "hello world",
            },
            200
        )
