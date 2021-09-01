## Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
## SPDX-License-Identifier: MIT-0

import json
import boto3
import base64
import os
import sys

kinesis_client = boto3.client('firehose')
kinesis_firehose = ''
if 'KINESIS_FIREHOSE_STREAM_NAME' in os.environ and os.environ['KINESIS_FIREHOSE_STREAM_NAME'].strip():
    kinesis_firehose = os.environ['KINESIS_FIREHOSE_STREAM_NAME'].strip()

def lambda_handler(event, context):

  try:
    row = '{"date":"'+ event["requestContext"]["time"] + '","ip":"' + event["headers"]["x-forwarded-for"] + '","userAgent":"' + event["headers"]["user-agent"] 
    row = row + '","userId":"' + event["queryStringParameters"].get("userid","unknown") + '","thirdPartyId":"' + event["queryStringParameters"].get("thirdpartyname","unknown") + '"}\n'
  
    kresponse = kinesis_client.put_record(DeliveryStreamName=kinesis_firehose,Record={'Data': row})
  except: #Catch all exceptions, we don't want the analytical part affects the business process so they are only printed in the logs
    print("Unexpected error:", sys.exc_info())
  

  response = {
  "statusCode": 200,
  "statusDescription": "200 OK",
  "isBase64Encoded": True,
  "headers": {
    "Content-Type": "image/gif"
    }
   }
  
  response['body'] = "R0lGODlhAQABAJAAAP8AAAAAACH5BAUQAAAALAAAAAABAAEAAAICBAEAOw=="

  return response
