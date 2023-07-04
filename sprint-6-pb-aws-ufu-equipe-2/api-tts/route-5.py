import json
from datetime import datetime
from utils import text_to_speech, insert_audio_in_bucket
from utils import insert_reference_in_dynamo

def route_5_handler(event, context):  
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
    audio_stream = text_to_speech(phrase)
    s3_response = insert_audio_in_bucket(phrase, audio_stream)

    current_date_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    insert_reference_in_dynamo(s3_response['id_hash'], phrase, s3_response['s3_obj_url'])
    
    response = {
        'statusCode': 200,
        'headers': {
            "Content-Type": "application/json",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },

        'body': {
            'received_phrase': phrase,
            'url_to_audio': s3_response['s3_obj_url'],
            'created_audio': current_date_time,
            'unique_id': s3_response['id_hash']      
        }

    }

    return response

