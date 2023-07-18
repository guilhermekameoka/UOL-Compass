import os
from boto3 import Session

region = os.environ['REGION']
session = Session(region_name= region)
polly = session.client("polly")

def text_to_speech(phrase):
    tts_response = polly.synthesize_speech(
        Engine='neural',
        OutputFormat='mp3',
        Text=phrase,
        LanguageCode='pt-BR',
        VoiceId='Thiago'
        )
    
    stream = tts_response['AudioStream']
    
    return stream