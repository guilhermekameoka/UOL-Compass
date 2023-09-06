import json
import boto3
import urllib3
from io import BytesIO


def rekognition_v1 (event, context):

    response =  event_request(event, "detect_labels", "labels")

    return response


def event_request(event: dict, detect_type: str, label_field: str) -> dict:
    """
    Builds a response based on label or face detection

    Attributes
    ----------
    event: dict
        serveless event
    detect_type: str
        Value passed to Rekognition (detect_labels, detect_faces)
    label_field: str
        Label name for json key
    """
    try:
        ebody = event.get('body')
        if not ebody:
            raise ValueError('Empty body received!! Please try again.')

        body_data = json.loads(ebody)
        bucket = body_data['bucket']
        imageURL = body_data['imageURL']

        imageName = body_data['imageName']

        url = imageURL
        
        http = urllib3.PoolManager()
        r = http.request('GET', url)

        s3 = boto3.client('s3')

        s3.upload_fileobj(BytesIO(r.data), bucket, imageName)

        s3file = s3.get_object(Bucket=str(bucket), Key=str(imageName))

        objects = rekognition_type(detect_type, bucket, imageName, {'MaxLabels': 10, 'MinConfidence': 60})
    
    except Exception as e:
        return error_message(str(e))

    body = construct_body(s3file, bucket, imageName)
    body.update({label_field: objects})

    response = {"statusCode": 200, "headers": {"Content-Type": "application/json"}, "body": json.dumps(body)}

    return response


def construct_body(s3file: dict, bucket: str, imageName: str) -> dict:
    """
    Builds a default body structure

    Attributes
    ----------
    s3file: dict
        S3 file from a bucket
    bucket: str
        Bucket name
    imageName: str
        Image name for url
    """    
    created = s3file["LastModified"].strftime("%d-%m-%Y %H:%M:%S")
    url_to_image = "https://"+str(bucket)+".s3.amazonaws.com/"+str(imageName)

    body = {
        "url_to_image": url_to_image,
        "created_image": created
    }

    return body


def error_message(message: str) -> dict:
    """
    Builds an error message and adds the right status code

    Attributes
    ----------
    message: str
        Error message
    status_code: int
        HTTP status code
    error_type: str
        Type of error
    """
    if 'NoSuch' in str(message):
        statusCode = 404
        error_type = "Not Found"
    elif 'bucket' in str(message) or 'imageName' in str(message):
        statusCode = 400
        message = "Wrong parameters, missing " + str(message)
        error_type = "Bad Request"
    else: 
        statusCode = 500
        error_type = "InternalServerError"
    
    body_message = {"message": message}
    response = {"statusCode": statusCode, "headers": {"Content-Type": "application/json"}, "body": json.dumps(body_message), "errorType": error_type}
    return response


def rekognition_type(detect_type: str, bucket: str, imageName: str, attributes: dict = {'MaxLabels':50, 'MinConfidence': 0}) -> list:
    """
    Builds a response based on a specific template for each Rekognition detection type

    Attributes
    ----------
    detect_type: str
        detect_labels or detect_faces
    bucket: str
        Bucket name that contains the image to be analyzed
    imageName: str
        Image name for Rekognition analysis
    """  
    rekognition = boto3.client('rekognition')

    if detect_type == "detect_labels":

        response = rekognition.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':imageName}}, MaxLabels=attributes['MaxLabels'], MinConfidence=attributes['MinConfidence'])

        print(json.dumps(response))

        labels = []
        for label in response['Labels']:
            item = { 
                "Confidence": label['Confidence'],
                "Name": label['Name']
            }
            labels.append(item)
        return labels

    elif detect_type == "detect_faces":
        
        response = rekognition.detect_faces(Image={'S3Object':{'Bucket':bucket,'Name':imageName}}, Attributes=['ALL'])
        print(json.dumps(response))
        
        faces = []
        for person in response['FaceDetails']:
            face = { 
                "position": {
                    "Height": person['BoundingBox']['Height'],
                    "Left": person['BoundingBox']['Left'],
                    "Top": person['BoundingBox']['Top'],
                    "Width": person['BoundingBox']['Width']
                },
                "classified_emotion": person['Emotions'][0]['Type'],
                "classified_emotion_confidence": person['Emotions'][0]['Confidence']
            }
            faces.append(face)

        if len(faces) == 0:
            face = { 
                "position": {
                    "Height": None,
                    "Left": None,
                    "Top": None,
                    "Width": None
                },
                "classified_emotion": None,
                "classified_emotion_confidence": None
            }
            faces.append(face)
        return faces
    
    else:
        raise Exception ('Wrong Rekognition parameter')