import json
from functions import *


valores = json_bucket_images(json.load(open('json_files/intent_expressar_info.json')))

#Checks for slots, validates values and return cards in case values are not valid
def validate_type_card(event, slots):

    #slot "voz" check and validation
    isMissing = check_missing_slot(slots, "voz", "PlainText", "Escolha sua voz") 

    if isMissing: 
        for key in valores['vozes']:
            rescard_title = ' '
            rescard_buttons = [
                {
                    "text": valores['vozes'][key]['texto'],
                    "value": key
                }
            ]
            imageUrl = valores['vozes'][key]['link']
            isMissing['messages'].append(build_message("ImageResponseCard", rescard_title, rescard_buttons, imageUrl))
        return isMissing
    
    if slots['voz']['value']['originalValue'] not in valores['vozes'].keys():
        return {'valid':False}
    
    #slot "desejo" check and validation
    isMissing = check_missing_slot(slots, "desejo", "PlainText", "O que você deseja expressar?") 

    if isMissing: 
        for key in valores['desejos']:
            rescard_title = ' '
            rescard_buttons = [
                {
                    "text": valores['desejos'][key]['texto'],
                    "value": key
                }
            ]
            imageUrl = valores['desejos'][key]['link']
            isMissing['messages'].append(build_message("ImageResponseCard", rescard_title, rescard_buttons, imageUrl))
        return isMissing
    
    desejo_opcao = str(slots['desejo']['value']['originalValue'])
    
    if desejo_opcao not in valores['desejos'].keys():
        return {'valid': False}

    #slot "escolha" check and validation
    isMissing = check_missing_slot(slots, "escolha", "PlainText", "O que você quer dizer?") 

    if isMissing: 
        for key in valores[desejo_opcao]:
            rescard_title = ' '
            rescard_buttons = [
                {
                    "text": valores[desejo_opcao][key]['texto'],
                    "value": key
                }
            ]
            imageUrl = valores[desejo_opcao][key]['link']
            isMissing['messages'].append(build_message("ImageResponseCard", rescard_title, rescard_buttons, imageUrl))
        return isMissing
    
    if slots['escolha']['value']['originalValue'] not in valores[desejo_opcao].keys():
        return {'valid': False}

    return {'valid': True}


def ObterExpressar_handler(event):

    intent = event['sessionState']['intent']['name']
    slots = event['sessionState']['intent']['slots']
    
    response = {}

    validation = validate_type_card(event, slots)

    #checks validation and invalid slots
    if event['invocationSource'] == 'DialogCodeHook':

        response = check_validation(validation, intent, slots)
        return response

    #all slots are valid
    if event['invocationSource'] == 'FulfillmentCodeHook':

        voz = slots['voz']['value']['originalValue']
        desejo = slots['desejo']['value']['originalValue']
        escolha = slots['escolha']['value']['originalValue']

        story = valores[desejo][escolha]['valor']

        if voz == 'menino':
            voice = 'Thiago'
        else:
            voice = 'Camila'
            story  = story+"!"

        audio_creation = create_audio(story,voice)
        audio = audio_creation['url_to_audio']

        audio_kommunicate = {
            "message": "<audio controls autoplay src='"+audio+"'></audio>",
            "platform": "kommunicate",
            "messageType": "html"
        }

        response = {
            "messages": [
                {
                    "contentType":"CustomPayload",
                    "content": json.dumps(audio_kommunicate)
                }
            ]
        }
        sessionState = close_session(intent, slots) 
        response.update(sessionState)

        final_message = end_card(" ")
        final_message["imageResponseCard"]['title'] = "O que você quer fazer?"
        response['messages'].append(final_message)
    
    return response
