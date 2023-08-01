import json


def health(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

def v1_description(event, context):
    body = {
        "message": "VISION api version 1."
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

def v2_description(event, context):
    body = {
        "message": "VISION api version 2."
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

import boto3
from datetime import datetime

def v1_vision_post(event, context):

    try:
        # Recuperar os dados do POST

        body = json.loads(event['body'])  # Converter a string JSON para um objeto Python
        #body = event['body']
        bucket = body['bucket']
        imageName = body['imageName']

        # Criar a URL da imagem
        #image_url = f"s3://{bucket}/{imageName}"
        image_url = f"https://{bucket}/{imageName}"

        # Inicializar o cliente do Rekognition
        rekognition_client = boto3.client('rekognition')

        # Chamar o Rekognition
        response = rekognition_client.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': imageName
                }
            }
        )

        # Log do resultado no CloudWatch
        print(response)

        # Criar a resposta a ser entregue
        labels = response['Labels']
        result = {
            "url_to_image": image_url,
            "created_image": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "labels": [{"Confidence": label["Confidence"], "Name": label["Name"]} for label in labels]
        }


        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }

    except KeyError as e:
        # Se houver um KeyError (campo faltando no JSON de entrada)
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid input JSON. Missing field: " + str(e)})
        }

    except Exception as e:
        # Para qualquer outra exceção não tratada
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error em post V1: " + str(e) + str(body)})
        }

import json
import boto3

def v2_vision_post(event, context):
    try:
        # Recuperar os dados do POST
        body = json.loads(event['body'])  # Converter a string JSON para um objeto Python
        bucket = body['bucket']
        imageName = body['imageName']

        # Criar a URL da imagem
        image_url = f"https://{bucket}/{imageName}"

        # Inicializar o cliente do Rekognition
        rekognition_client = boto3.client('rekognition')

        # Chamar o Rekognition
        response = rekognition_client.detect_faces(
            Image={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': imageName
                }
            },Attributes=['ALL']
        )

        # Log do resultado no CloudWatch
        print(json.dumps(response, indent=4))
        result = json.dumps(response)

       # Processar a resposta para obter os detalhes desejados
        faces_data = []
        if 'FaceDetails' in response and len(response['FaceDetails']) > 0:
            for face in response['FaceDetails']:
                if 'BoundingBox' in face:
                    position = {
                        "Height": face['BoundingBox']['Height'],
                        "Left": face['BoundingBox']['Left'],
                        "Top": face['BoundingBox']['Top'],
                        "Width": face['BoundingBox']['Width']
                    }

                    classified_emotion = None
                    classified_emotion_confidence = None

                    if 'Emotions' in face and len(face['Emotions']) > 0:
                        max_emotion = max(face['Emotions'], key=lambda x: x['Confidence'])
                        classified_emotion = max_emotion['Type']
                        classified_emotion_confidence = max_emotion['Confidence']

                    face_data = {
                        "position": position,
                        "classified_emotion": classified_emotion,
                        "classified_emotion_confidence": classified_emotion_confidence
                    }
                    faces_data.append(face_data)
        else:
            # Se não houver face, adicionar a resposta vazia ao resultado
            position = {
                "Height": None,
                "Left": None,
                "Top": None,
                "Width": None
            }
            face_data = {
                "position": position,
                "classified_emotion": None,
                "classified_emotion_confidence": None
            }
            faces_data.append(face_data)

        result = {
            "url_to_image": image_url,
            "created_image": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "faces": faces_data
        }

        # Log do resultado no CloudWatch
        print(json.dumps(result, indent=4))

        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }

    except KeyError as e:
        # Se houver um KeyError (campo faltando no JSON de entrada)
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid input JSON. Missing field: " + str(e)})
        }

    except Exception as e:
        # Para qualquer outra exceção não tratada
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error em post V2: " + str(e) + str(body)})
        }