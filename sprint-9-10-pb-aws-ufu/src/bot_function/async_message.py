import json
import urllib3
import os
import random
from functions import create_audio, create_story_function, send_kommunicate_msg


def lambda_handler(event, context):
    """
    Handler asyncronous function,
    expected keys are: body, phase and id_model

    """
    
    try:
        body = event.get('body')
        phrase = event.get('phrase')
        id_model = event.get('id_model')

        story = create_story_function(phrase, id_model)

        voice = ['Camila','Thiago']
        audio_creation = create_audio(story,voice[random.randint(0, len(voice)-1)])
        audio = audio_creation['url_to_audio']

        groupId = body['requestAttributes']['groupId']
        message = "<img src='https://"+os.environ['BUCKET_IMAGES']+".s3.amazonaws.com/loaded.png'><br><audio controls src='"+audio+"'></audio><br>Aqui está a história que criamos!"
        fromUserName = body['requestAttributes']['botId']
        contentType =  "3"
        
        send_kommunicate_msg(groupId,message,fromUserName,contentType)

        message = story
        res = send_kommunicate_msg(groupId,message,fromUserName,contentType)
        return(res.status)

    except Exception as e:
        return e

