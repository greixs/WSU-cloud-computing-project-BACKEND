import json
import ast

def lambda_handler(event, context):
    # TODO implement

    # parsed = json.loads(event[0])

    sorted_price = sorted(event, key=lambda d: float(d['price']))

    return {
        'statusCode': 200,
        'body': json.dumps(sorted_price)
    }
