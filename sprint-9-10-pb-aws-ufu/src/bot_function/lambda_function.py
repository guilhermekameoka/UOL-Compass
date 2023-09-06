from intent_historia import *
from intent_historia_cards import *
from intent_expressar import *

#checks intent and call the appropriate functions
def lambda_handler(event, context):

    intent = event['sessionState']['intent']['name']
    
    response = {}

    if intent == 'ObterHistoria':
        response = ObterHistoria_handler(event)

    if intent == 'ObterHistoriaCards':
        response = ObterHistoriaCards_handler(event)

    if intent == 'ObterExpressar':
        response = ObterExpressar_handler(event)

    return response
