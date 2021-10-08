import json
import requests

def lambda_handler(event, context):
    # TODO implement
    pid = event.get("woolies")

    headers = {
                "content-type": "application/json",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.32 Safari/537.36"
    }

    get = requests.get(f"https://www.woolworths.com.au/api/v3/ui/schemaorg/product/{pid}", headers=headers)
    json_data = get.json()

    product = json_data['offers']
    price = product['price']
    name = json_data['name']
    img = json_data['image']
    print(product)

    return {
        'statusCode': 200,
        "name": name,
        "price": price,
        "img": img
    }
