import json
from datetime import datetime
from utils import text_to_speech, insert_audio_in_bucket

def route_4_handler(event, context):
    json_body = json.loads(event['body'])
    try:
        phrase = json_body['phrase']
    except:
        body = {'errorMsg': 'Invalid phrase request.'}
        return {'statusCode': 500, 'body': json.dumps(body)}
 
    audio_stream = text_to_speech(phrase)
    s3_response = insert_audio_in_bucket(phrase, audio_stream)

    current_date_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    
    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': {
            'received_phrase': phrase,
            'url_to_audio': s3_response['s3_obj_url'],
            'created_audio': current_date_time
        }        
    }
    
    return response