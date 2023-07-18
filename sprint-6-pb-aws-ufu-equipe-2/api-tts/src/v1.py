import json
from datetime import datetime
import polly
import s3

def v1_tts(event, context):
    json_body = json.loads(event['body'])
    
    try:
        phrase = json_body['phrase']
    except:
        response = {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
            },

            'body': json.dumps({
                'message': 'Invalid phrase request!'
            })
        }
    
        return response
 
    audio_stream = polly.text_to_speech(phrase)
    s3_response = s3.insert_audio_in_bucket(phrase, audio_stream)

    current_date_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    
    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST'
        },
        'body': json.dumps({
            'received_phrase': phrase,
            'url_to_audio': s3_response['s3_obj_url'],
            'created_audio': current_date_time
        })      
    }
    
    return response