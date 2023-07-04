from datetime import datetime
from boto3 import Session
from boto3 import resource
import hashlib

session = Session(region_name= 'us-east-1')
polly = session.client("polly")
s3 = resource('s3')
# bucket_name = os.environ['BUCKET_NAME']
bucket_name = 'sprint6-polly'
bucket = s3.Bucket(bucket_name)

def text_to_speech(phrase):
    tts_response = polly.synthesize_speech(
        OutputFormat='mp3',
        Text=phrase,
        LanguageCode='pt-PT',
        VoiceId='Ines'
        )
    stream = tts_response['AudioStream']
    return stream

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

def insert_reference_in_dynamo(id_hash, phrase, s3_obj_url):
    dynamodb = resource('dynamodb')
    table = dynamodb.Table('sprint6teste')

    table.put_item(
        Item = {
            'id': id_hash,
            'phrase': phrase,
            'url': s3_obj_url,
        }
    )

def check_existing_phrase(id_hash):
    dynamodb = resource('dynamodb')
    table = dynamodb.Table('sprint6teste')

    response = table.get_item(Key={'id': id_hash})
    return response.get('Item')