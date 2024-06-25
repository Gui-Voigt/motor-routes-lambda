import json
import base64

API_KEY = "AIzaSyA3asDMh0MJ2S9G9XH3LDDr6p30E9vG39k"
endpointRoutes = "https://routes.googleapis.com/directions/v2:computeRoutes"

print(API_KEY)

def lambda_handler(event, context):
    try:
        body_encoded = event['body']
        body_decoded = base64.b64decode(body_encoded)
        
        body = json.loads(body_decoded)
        print(body)

        # Extrai os dados dos objetos recebidos
        origem = body['origem']
        destino = body['destino']

        # VERIFICAÇÕES DE ENTRADAS
        if 'id' not in origem or 'lat' not in origem or 'long' not in origem:
            raise KeyError("Dados de origem estão incompletos")

        if 'id' not in destino or 'lat' not in destino or 'long' not in destino:
            raise KeyError("Dados de destino estão incompletos")

        resultado = {
            'id': origem['id'],  # Mantém o 'id' do primeiro objeto
            'resume': destino['resume'],
            'rotas': []  # Adiciona o atributo 'rotas' como um array vazio
        }
        
        inputRoutes = {
            "origin": {
                "location": {"latLng": {"latitude": origem['lat'], "longitude": origem['long']}}
            },
            "destination": {
                "location": {"latLng": {"latitude": destino['lat'], "longitude": destino['long']}}
            },
            "travelMode": "DRIVE",
            "routingPreference": "TRAFFIC_AWARE",
            "polylineQuality": "HIGH_QUALITY"
        }

        # CHAMADA DE ROTAS
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": API_KEY,
            "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline",
        }

        # Retorna uma resposta de sucesso com o resultado
        return {
            'statusCode': 200,
            'body': json.dumps(resultado)
        }

    except KeyError as e:
        # Retorna uma resposta de erro em caso de campos faltantes
        return {
            'statusCode': 400,  # Bad Request
            'body': json.dumps({'Error.:': str(e)})
        }

    except json.JSONDecodeError:
        # Retorna uma resposta de erro em caso de dados JSON inválidos
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Dados JSON inválidos'})
        }
