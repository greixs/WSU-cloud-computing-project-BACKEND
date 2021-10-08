import json
import requests
import certifi

import ssl


def lambda_handler(event, context):
    # TODO implement
    # https://shop.coles.com.au/search/resources/store/20601/productview/bySeoUrlKeyword/lime-mandarin-hand-wash
    pid = event.get("coles")
    url = f"https://shop.coles.com.au/search/resources/store/20601/productview/bySeoUrlKeyword/{pid}"

    print(ssl.OPENSSL_VERSION)

    cafile = certifi.where()

    headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "en-US,en;q=0.9",
            'User-Agent'         : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
    }

    print(cafile)
    print(url)
    # proxies={"https":"https://frenox:trenox@43.229.61.124:3128"}
    get = requests.get(url, headers=headers, proxies={"https":"http://frenox:trenox@43.229.61.124:3128"})
    print(get.text)
    json_data = get.json()

    price = json_data.get("catalogEntryView")[0].get("p1").get("o")
    name = json_data.get("catalogEntryView")[0].get("s").replace("-", " ")
    img = "https://shop.coles.com.au/" + json_data.get("catalogEntryView")[0].get("t")

    return {
        'statusCode': 200,
        'name': name,
        'price': price,
        'img': img
    }
