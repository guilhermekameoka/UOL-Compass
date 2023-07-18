import json
import boto3
from datetime import datetime
import polly
import s3
import dynamo

def v3_tts(event, context):
    json_body = json.loads(event['body'])
    try:
        phrase = json_body['phrase']
    except:
        body = {
            "errMsg": "Invalid phrase"
        }
        response = {
            "statusCode": 500,
            "body": json.dumps(body)
        }
        return response
    
    id_hash = s3.get_id_hash(phrase)
    existing_item = dynamo.check_existing_phrase(id_hash)
    if existing_item:
        response = {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
                'body': json.dumps({
                    'received_phrase': existing_item['phrase'],
                    'url_to_audio': existing_item['url'],
                    'unique_id': existing_item['id']
                })      
            }
    else:
        audio_stream = polly.text_to_speech(phrase)
        s3_response = s3.insert_audio_in_bucket(phrase, audio_stream)
        dynamo.insert_reference_in_dynamo(s3_response['id_hash'], 
                                          phrase, 
                                          s3_response['s3_obj_url'])

        current_date_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
 
        response = {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({
                'received_phrase': phrase,
                'url_to_audio': s3_response['s3_obj_url'],
                'created_audio': current_date_time,
                'unique_id': s3_response['id_hash']  
            })
                    
        }
    return response