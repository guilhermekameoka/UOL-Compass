import json
import boto3
import os
from contextlib import closing
import hashlib


def unique_str_id(string: str, last_idx: int = 12) -> str:
    m = hashlib.md5()
    string = string.encode('utf-8')
    m.update(string)
    unique_name: str = str(int(m.hexdigest(), 16))[0:last_idx]
    return unique_name


def convert_save_audio (received_phrase, type_voice):

    s3 = boto3.client('s3')

    # Breaking text for conversion
    rest = received_phrase
    textBlocks = []
    while (len(rest) > 1100):
        begin = 0
        end = rest.find(".", 1000)

        if (end == -1):
            end = rest.find(" ", 1000)

        textBlock = rest[begin:end]
        rest = rest[end:]
        textBlocks.append(textBlock)
    textBlocks.append(rest)

    # Converting text to audio with Polly
    voice = type_voice
    postId = unique_str_id(received_phrase)

    try:
        object = s3.get_object(Bucket = os.environ['BUCKET_POLLY'], Key=postId + ".mp3")
        return postId
    
    except:
        pass

    polly = boto3.client('polly')

    for textBlock in textBlocks:
        response = polly.synthesize_speech(
            Engine='neural',
            OutputFormat='mp3',
            Text=textBlock,
            VoiceId=voice
        )
        # Save the audio stream returned by Amazon Polly on Lambda's temp
        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                output = os.path.join("/tmp/", postId)
                with open(output, "ab") as file:
                    file.write(stream.read())

    # Uploading the mp3 file to the s3 bucket
    s3.upload_file('/tmp/' + postId,
                os.environ['BUCKET_POLLY'],
                postId + ".mp3")
    s3.put_object_acl(ACL='public-read',
                    Bucket=os.environ['BUCKET_POLLY'],
                    Key=postId + ".mp3")
    
    return postId


def polly_v1 (event, context):

    # check if phrase keys are present
    try:
        ebody = event['body']
        received_phrase = json.loads(ebody)['phrase']
        
    except:
        message = {"message":"Wrong parameters"}
        response = {"statusCode": 500, "headers": {"Content-Type": "application/json"}, "body": json.dumps(message)}
        return response

    type_voice = 'Camila'
    
    try:
        type_voice = json.loads(ebody)['voice']

    except:
        pass

    s3 = boto3.client('s3')
    
    try:

        postId = convert_save_audio(received_phrase, type_voice)

        location = s3.get_bucket_location(Bucket=os.environ['BUCKET_POLLY'])
        region = location['LocationConstraint']

        if region is None:
            url_begining = "https://"+str(os.environ['BUCKET_POLLY'])+".s3.amazonaws.com"
        else:
            url_begining = "https://"+str(os.environ['BUCKET_POLLY'])+".s3-" + str(region) + ".amazonaws.com" 

        url = url_begining + "/" + str(postId) + ".mp3"


        # Checking last Modified file info and converting
        response = s3.get_object(Bucket = os.environ['BUCKET_POLLY'], Key=postId + ".mp3")
        created_audio = response["LastModified"].strftime("%d-%m-%Y %H:%M:%S")

        body = {"received_phrase": received_phrase,
                "url_to_audio": url,
                "created_audio": created_audio}

        response = {"statusCode": 200,
                    "headers": {
                        "Content-Type": "application/json"
                    },
                    "body": json.dumps(body)}   
    
    except:
        
        message = {"message":"Internal Error"}
        response = {"statusCode": 500, "headers": {"Content-Type": "application/json"}, "body": json.dumps(message)}

    return response