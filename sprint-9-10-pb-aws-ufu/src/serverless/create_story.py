import json
import urllib3


def create_story_v1 (event, context):

    # check if phrase key is present
    try:
        ebody = event['body']
        received_phrase = json.loads(ebody)['phrase']
        KEY_API = json.loads(ebody)['key']
        id_model = json.loads(ebody)['id_model']

        http = urllib3.PoolManager()
        url = 'https://api.openai.com/v1/chat/completions'

        Headers = {'Authorization' : f'Bearer {KEY_API}', 'Content-Type': 'application/json'}
        payload = {'model': id_model, 'messages': [{'role': 'user', 'content': received_phrase}]}
  
        encoded_body = json.dumps(payload)
        res = http.request('POST', url, body=encoded_body, headers=Headers)
       
        respo = ''
        
        if res.status == 200:
            respo = json.loads(res.data)

        else:
            raise Exception ('Was not able to get a proper message')
        
        story = respo['choices'][0]['message']['content']
    
        story = {"story":story}
        response = {"statusCode": 200, "headers": {"Content-Type": "application/json"}, "body": json.dumps(story)}

    except:
        
        message = {"message":"Internal Error"}
        response = {"statusCode": 500, "headers": {"Content-Type": "application/json"}, "body": json.dumps(message)}

    return response