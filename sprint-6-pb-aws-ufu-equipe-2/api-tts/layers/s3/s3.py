import os
from boto3 import Session
from boto3 import resource
import hashlib

region = os.environ['REGION']
session = Session(region_name= region)

polly = session.client("polly")

s3 = resource("s3")
bucket_name = os.environ['BUCKET_NAME']
bucket = s3.Bucket(bucket_name)


def get_id_hash(phrase):
    id_hash = hashlib.sha256(phrase.encode()).hexdigest()
    return id_hash

def insert_audio_in_bucket(phrase, audio_stream):
    id_hash = get_id_hash(phrase)
    file_name = f"{id_hash}.mp3"
    s3_obj_url = f'https://{bucket_name}/{file_name}'

    bucket.put_object(Key=file_name, Body=audio_stream.read())   

    response = {
        's3_obj_url': s3_obj_url,
        'id_hash': id_hash
    }

    return response