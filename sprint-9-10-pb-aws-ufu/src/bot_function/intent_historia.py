import json
import urllib3
from functions import *
import random
import boto3
import os

ASYNC_FUNCTION_NAME = os.environ['ASYNC_FUNCTION_NAME']
    
#Checks for slots, validates values and return cards in case values are not valid
def validate_type_card(event, slots):

    valid_types = ['kommunicateMediaEvent']

    #slot historia check and validation
    isMissing = check_missing_slot(slots, "historia", "PlainText", "Insira uma imagem ou tire uma foto do seu desenho") 
    if isMissing: return isMissing

    if slots['historia']['value']['originalValue'] not in valid_types:
        #Amazon lex tests exclusive
        if "http" not in slots['historia']['value']['originalValue']:
            content = "Por favor selecione uma imagem"
            response = build_response("historia", content)
            return response
        
    elif 'image/jpeg' not in str(json.loads(event['requestAttributes']['attachments'])[0]['type']):
        if 'image/png' not in str(json.loads(event['requestAttributes']['attachments'])[0]['type']):
            print(str(json.loads(event['requestAttributes']['attachments'])[0]['type']))
            content = "Por favor selecione um tipo de arquivo de imagem no formato jpeg ou png"
            response = build_response("historia", content)
            return response
   
    return {'valid': True}


def ObterHistoria_handler(event):

    intent = event['sessionState']['intent']['name']
    slots = event['sessionState']['intent']['slots']
    
    print(json.dumps(event))

    response = {}

    validation = validate_type_card(event, slots)

    #checks validation and invalid slots
    if event['invocationSource'] == 'DialogCodeHook':

        response = check_validation(validation, intent, slots)
        return response

    #all slots are valid
    if event['invocationSource'] == 'FulfillmentCodeHook':

        slot_historia = slots['historia']['value']['originalValue']
        
        try:
            imageURL = str(json.loads(event['requestAttributes']['attachments'])[0]['payload']['url'])

        except:
            imageURL = slot_historia

        http = urllib3.PoolManager()
        url = os.environ['INVOKE_URL']+"/rekognition/v1"

        # imageName = "imageTest2.jpg"
        imageName = str(json.loads(event['requestAttributes']['attachments'])[0]['payload']['name'])

        Headers = {'Content-Type': 'application/json'}
        payload = {
            "bucket": os.environ['BUCKET_IMAGES'],
            "imageURL": imageURL,
            "imageName": imageName
        }

        encoded_body = json.dumps(payload)
        res = http.request('POST', url, body=encoded_body, headers=Headers)
        respo = ''

        if res.status == 200:
            respo = json.loads(res.data)

        labels = []
        for label in respo['labels']:
            labels.append(label['Name'])

        if len(labels) == 0:
            labels = ['Hero']

        translated_labels = ",".join(labels)
        translated_labels = translate(translated_labels)
        translated = translated_labels.split(',')

        print(translated)    
        
        #random index----------------------------------------
        rand_number = lambda: random.randint(0, len(labels)-1)
        #----------------------------------------------------

        label1 = translated[rand_number()]
        label2 = translated[rand_number()]
        label3 = translated[rand_number()]
        label4 = translated[rand_number()]

        id_model = 'gpt-3.5-turbo'
        phrase = f'crie uma história infantil bem curta, máximo de 500 caracteres e não ultrapasse 80 palavras, que contenha os seguintes elementos: {label1},{label2},{label3},{label4}'

        #async function -------------------------------------------------------------------------------------------
        client = boto3.client('lambda')
        client.invoke(
            FunctionName=ASYNC_FUNCTION_NAME,
            InvocationType='Event',
            Payload = bytes(json.dumps({'body': event, 'phrase' : phrase, 'id_model' : id_model}), encoding='utf-8')
        )
        #-----------------------------------------------------------------------------------------------------------

        image_kommunicate = {
            "message": "<img src='https://"+os.environ['BUCKET_IMAGES']+".s3.amazonaws.com/loading.gif'><br>Estou pensando em uma história, talvez demore alguns segundos... vamos fazer outra coisa enquanto isso?",
            "platform": "kommunicate",
            "messageType": "html"
        }

        response = {
            "messages": [
                {
                    "contentType":"CustomPayload",
                    "content": json.dumps(image_kommunicate)
                }
            ]
        }
        sessionState = close_session(intent, slots) 
        response.update(sessionState)

        final_message = end_card(" ")
        final_message["imageResponseCard"]['title'] = "O que você quer fazer?"
        response['messages'].append(final_message)
    
    return response
