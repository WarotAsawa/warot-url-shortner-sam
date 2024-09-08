import json
import boto3
from botocore.exceptions import ClientError

# import requests


def lambda_handler(event, context):

    urlPath = event['path'].split('/', 1)[1]
    redirectedURL = queryDynamoDB("warot-short-url-table", urlPath, "redirect")
    print(redirectedURL)
    return {
        "isBase64Encoded": False,
        "statusCode": 302,
        "headers": {
            "Location": redirectedURL
        },
        "multiValueHeaders": {},
        "body": ""
    }

# A function to getItem from DynamoDB Table with selected key

def queryDynamoDB(tableName, urlPath, field):
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
    table = dynamodb.Table(tableName)
    print(tableName)
    print(urlPath)
    try:
        response = table.get_item(
            Key={
                'url': urlPath
            }
        )
        item = response.get('Item')
        
        print(item)
        if item is None:
            return "https://www.google.com/search?q="+urlPath
        return item[field]
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        print(error_code)
        print(error_message)
        
        return "https://www.google.com/search?q="+urlPath
