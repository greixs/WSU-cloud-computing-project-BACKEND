import json

# sample
OPTIONS = {
        "banana": {"woolies": "133211", "coles":"coles-fresh-bananas---loose"},
        "apple": {"woolies": "105919", "coles":"apples-pink-lady-loose"},
        "chicken breast": {"woolies": "710953", "coles":"coles-rspca-free-range-chicken-breast-single"},
    }

def lambda_handler(event, context):
    # TODO implement
    # {"item" :"Banana"}

    item = event.get("item").lower()

    # check if the received json have the item name
    if item not in OPTIONS:
        return {
            'statusCode': 405,
            'body': json.dumps(f'{item} not in the options')
        }


    return {
        'statusCode': 200,
        'body': json.dumps(OPTIONS[item])
    }
