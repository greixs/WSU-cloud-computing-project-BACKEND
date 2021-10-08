import json

# sample
OPTIONS = {
        "banana": {"woolies": "133211", "coles":"coles-fresh-bananas---loose"},
    }

def lambda_handler(event, context):
    # TODO implement

    item = event.get("item").lower()

    # check if the received json have the item name
    if item not in OPTIONS:
        return {
            'statusCode': 405,
            'body': json.dumps(f'{item} not in the options')
        }


    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }
