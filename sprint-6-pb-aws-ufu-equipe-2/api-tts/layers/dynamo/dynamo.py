import os
import json
from boto3 import Session
from boto3 import resource

region = os.environ['REGION']
session = Session(region_name= region)

polly = session.client("polly")

s3 = resource("s3")
bucket_name = os.environ['BUCKET_NAME']
bucket = s3.Bucket(bucket_name)

dynamodb = resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def insert_reference_in_dynamo(id_hash, phrase, s3_obj_url):
    table.put_item(
        Item = {
            'id': id_hash,
            'phrase': phrase,
            'url': s3_obj_url,
        }
    )

def check_existing_phrase(id_hash):
    response = table.get_item(Key={'id': id_hash})
    return response.get('Item')