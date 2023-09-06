import json
import urllib3
import http.client
import os


RAPID_API = os.environ['RAPID_API']
BUCKET_IMAGES = os.environ['BUCKET_IMAGES']


def json_bucket_images (json_info):
    """
    changes bucket_name to the one specified in bot.conf,
    which is the bucket name where the image files are.
    The files in json_files have a generic bucket name.

    Attributes
    ----------
    json_info: dict
        json structure to have the bucket name change
    """
    for key in json_info:
        for value in json_info[key].values():
            value['link'] = value['link'].replace('meu_bucket', BUCKET_IMAGES)
    
    return json_info

#checks if there are missing slots and returns the slot to elicit
def check_missing_slot(slots, invalidSlot, contentType, content, force_return = False):
    """
    check for missing slots

    Attributes
    ----------
    slots: dict
        intents slots
    invalidSlot: str
        name of invalid slot
    contentType: str
        type of content, ex: PlainText
    content: str
        message to return
    """

    if not slots[invalidSlot] or force_return == True:
        return {
            'valid': False,
            'invalidSlot': invalidSlot,
            'messages': [
                {
                    "contentType":contentType,
                    "content": content,
                }
            ]
        }
    else:
        return False 


def build_responsecard (invalidSlot, contentType, content, subtitle, buttons, imageUrl = None ):
    """
    builds a responsecard to the slot to elicit 

    Attributes
    ----------
    invalidSlot: str
        name of invalid slot
    contentType: str
        type of content, ex: PlainText
    content: str
        message to return
    subtitle: str
        card subtile
    buttons: str
        card buttons
    imageUrl: str
        image card Url to display
    """

    response = {
        "valid": False,
        "invalidSlot": invalidSlot,
        "messages": [
            {
                "contentType": contentType,
                "content": content,
                contentType[0].lower() + contentType[1:]: {
                    "title": " ",
                    "subtitle": " ",
                    "imageUrl": imageUrl,
                    "buttons": buttons
                }
            }
        ]
    }

    return response


def build_message (contentType, subtitle, buttons, imageUrl = None ):
    """
    builds a generic lex message

    Attributes
    ----------
    contentType: str
        type of content, ex: PlainText
    subtitle: str
        card subtile
    buttons: str
        card buttons
    imageUrl: str
        image card Url to display
    """
    message = {
        "contentType": contentType,
        contentType[0].lower() + contentType[1:]: {
            "title": " ",
            "subtitle": subtitle,
            "imageUrl": imageUrl,
            "buttons": buttons
        }
    }
    return message


def build_response(invalidSlot, content):
    """
    builds a generic PlainText lex message with validation and slot to elicit

    Attributes
    ----------
    invalidSlot: str
        invalid slot to elicit
    content: str
        content of the PlainText message
    """

    response = {
        "valid": False,
        "invalidSlot": invalidSlot,
        "messages": [
            {
                "contentType": "PlainText",
                "content": content
            }
        ]
    }

    return response


def check_validation (validation, intent, slots):
    """
    build a response based on validation value, valid or invalid

    Attributes
    ----------
    validation: bool
        valid is True or False
    intent: str
        intent name
    slots: dict
        intent slots of incoming event
    """

    if validation['valid'] == False:
        response = {
            "sessionState": {
                "dialogAction": {
                    "slotToElicit": validation['invalidSlot'],
                    "type": "ElicitSlot"
                },
                "intent": {
                    "name": intent,
                    "slots": slots
                }
            },
            "messages": validation['messages']
        }
    else:
        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Delegate"
                },
                "intent": {
                    "name": intent,
                    "slots": slots
                }
            }
        }
    return response


def close_session(intent, slots):
    """
    sessionState type close and state fulfilled

    Attributes
    ----------
    intent: str
        intent name
    slots: dict
        intent slots of incoming event
    """
    
    sessionState = {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                "name": intent,
                "slots": slots,
                "state": "Fulfilled"
            }
        }
    }
    return sessionState


def end_card(title):
    """
    Final card response

    Attributes
    ----------
    title: str
        title name
    """

    rescard_title = title
    rescard_buttons = [
        {
            "text": 'Desenho - Foto',
            "value": 'desenho'
        },
        {
            "text": 'Cartões',
            "value": 'cartões'
        },
        {
            "text": 'Expressar',
            "value": 'expressar'
        },
    ]
    imageUrl = 'https://'+BUCKET_IMAGES+'.s3.amazonaws.com/bot.jpg'
    return (build_message("ImageResponseCard", rescard_title, rescard_buttons, imageUrl))


def create_audio (phrase, voice):
    """
    Texto to Audio conversion of a given phrase and selected voice

    Attributes
    ----------
    phrase: str
        phrase to be converted
    voice: str
        polly Neural voice to be used
    """

    http = urllib3.PoolManager()
    url = os.environ['INVOKE_URL']+"/polly"

    Headers = {'Content-Type': 'application/json'}
    payload = {
        "phrase": phrase,
        "voice": voice
    }

    encoded_body = json.dumps(payload)
    res = http.request('POST', url, body=encoded_body, headers=Headers)
    response = ''
    if res.status == 200:
        response = json.loads(res.data)

    return response



#translates for the language selected
def translate(text, language = 'pt-br'):
    """
    Text translation, requires an Api key from rapidapi.com

    Attributes
    ----------
    text: str
        phrase to be translated
    language: str
        language output, pt-br is default, change it to translate texto to another language
    """

    try:
        conn = http.client.HTTPSConnection("microsoft-translator-text.p.rapidapi.com")
        payload = [
            {
                "Text": text
            }
        ]
        headers = {
            'content-type': "application/json",
            'X-RapidAPI-Key': RAPID_API,
            'X-RapidAPI-Host': "microsoft-translator-text.p.rapidapi.com"
        }
        if(language == 'pt-br'):
            conn.request("POST", "/translate?to%5B0%5D=pt-br&api-version=3.0&profanityAction=NoAction&textType=plain", json.dumps(payload), headers)
        
        else:
            conn.request("POST", "/translate?to%5B0%5D=en&api-version=3.0&from=pt-br&profanityAction=NoAction&textType=plain", json.dumps(payload), headers)
        res = conn.getresponse()
        data = res.read()
        response = json.loads(data.decode('utf-8'))
        translated_text = response[0]['translations'][0]['text']
        return translated_text
    
    except:
        return text
    

def create_story_function (phrase, id_model):
    """
    Story creation with a given phrase and an id_model for openAi

    Attributes
    ----------
    phrase: str
        story phrase to input
    id_model: str
        openAi ID model that will be used

    """

    http = urllib3.PoolManager()
    url = 'https://api.openai.com/v1/chat/completions'

    KEY_API = os.environ['KEY_API_OPENAI']
    Headers = {'Authorization' : f'Bearer {KEY_API}', 'Content-Type': 'application/json'}
    payload = {'model': id_model, 'messages': [{'role': 'user', 'content': phrase}]}

    encoded_body = json.dumps(payload)
    res = http.request('POST', url, body=encoded_body, headers=Headers)
    response = ''
    if res.status == 200:
        response = json.loads(res.data)

    story = response['choices'][0]['message']['content']
    return story


def send_kommunicate_msg (groupId, message, fromUserName, contentType):
    """
    send message to chatbot via kommunicate

    Attributes
    ----------
    groupId: str
        bot group unique ID
    message: str
        message to send
    fromUserName: str
        User sending, select bot name for responses
    contentType: str
        DEFAULT(0) | ATTACHMENT(1) | LOCATION(2) | TEXT_HTML(3) | PRICE(4) | IMAGELINK(5) | HYPERLINK(6) 

    """

    http = urllib3.PoolManager()
    url = 'https://services.kommunicate.io/rest/ws/message/v2/send'

    platform = "kommunicate"

    KEY_API = os.environ['KEY_API_KOM']
    Headers = {'Api-Key' : f'{KEY_API}', 'Content-Type': 'application/json'}

    payload = { 
        "groupId": groupId, 
        "message":message,
        "fromUserName":fromUserName,
        "contentType": contentType,
        "platform": platform
    }

    encoded_body = json.dumps(payload)
    res = http.request('POST', url, body=encoded_body, headers=Headers)
    return res