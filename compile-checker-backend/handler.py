import json
import os
from secret import SECRET
import base64
from uuid import uuid4

def hello(event, context):
    body = {
        "message": "Go Serverless v2.0! Your function executed successfully!",
        "input": event,
    }
    response = {"statusCode": 200, "body": json.dumps(body)}
    return response

def compile(event, context):
    body = json.loads(event['body'])
    if body.get('secret', '') != SECRET:
        return {
            "statusCode": 403,
            "body": json.dumps({
                "message": "Invalid secret",
                "input": event,
            }),
            "headers": {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            }
        }
    source = body.get('source', '')
    file_name = str(uuid4())
    with open(f'/tmp/{file_name}.cpp', 'w') as f:
        f.write(source)
    os.system(f'g++ -std=c++17 -O2 -static /tmp/{file_name}.cpp -o /tmp/{file_name}')
    with open(f'/tmp/{file_name}', 'rb') as f:
        output_file_content = base64.b64encode(f.read()).decode('utf-8')
    os.remove(f'/tmp/{file_name}.cpp')
    os.remove(f'/tmp/{file_name}')
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": output_file_content,
            "input": event,
        }),
        "headers": {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }
    }