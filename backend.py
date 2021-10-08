"""
    woolies: https://www.woolworths.com.au/apis/ui/Search/products (straight up json)
    coles: https://shop.coles.com.au/online/COLRSSearchDisplay?storeId=20601&catalogId=10576&searchTerm=banana&categoryId=&tabType=everything&tabId=everything&personaliseSort=false&langId=-1&beginIndex=0&browseView=false&facetLimit=100&searchSource=Q&sType=SimpleSearch&resultCatEntryType=2&showResultsPage=true&pageView=image&errorView=AjaxActionErrorResponse&requesttype=ajax (you need lxml html parse and find the "product", then there will be an array of dict for you to parse)
"""
import requests
import json
from thread_utils.session_handler import get_session
from collections import OrderedDict

def get_woolies(event):
    pid = event.get("woolies")

    headers = {
             "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "en-US,en;q=0.9",
            'User-Agent'         : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',

            # "accept": "application/json, text/plain, */*",
            # "accept-language": "en-US,en;q=0.9",
            # # "cache-control": "no-cache",
            # # "pragma": "no-cache",
            # # "content-type": "",
            # 'User-Agent'         : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
            # 'Referer'            : 'https://www.footlocker.com.au/en/homepage',
            # 'Cookie'             : 'dtSa=-; RT="z=1&dm=www.woolworths.com.au&si=073e38be-5b22-4385-b745-416da5339ac6&ss=kuhvwbds&sl=2&tt=ht&rl=1&obo=1&ld=3jop&r=286w3hau&ul=3jop"; dtCookie=v_4_srv_2_sn_CE3EA42298490A389003ABC26EE97557_app-3A5cc956099f88e4b7_0_app-3Af908d76079915f06_1_ol_0_perc_100000_mul_1; AKA_A2=A; bff_region=syd2; akaalb_woolworths.com.au=~op=www_woolworths_com_au_ZoneA:PROD-ZoneA|www_woolworths_com_au_BFF_SYD2:WOW-BFF-SYD2|www_woolworths_com_au_BFF_SYD_Launch:WOW-BFF-SYD2|~rv=60~m=PROD-ZoneA:0|WOW-BFF-SYD2:0|~os=43eb3391333cc20efbd7f812851447e6~id=a3530e61ef8b982e9e0a14d1757fd52c; _abck=F088A0F12E5A6F284AD0736EF301B048~0~YAAQAwUgFw+pp1R8AQAA/Oc3XgZB4SGg47G1uc9ywNhzSg3i2seEBbSCq5ZZfb00n7wrEd4bc8R0q3oE5pVK7+E5rUtSYi1G9svxnbWs5G2aijMkmNvEIdu4Xjunv1wSb+zzdtQ3jAVn5W7TFVIb9/iX2wHL070KgAUcu952SJ8lAb30/bm00oM5D0AJDX3i32kb3u8FVre0Nc/1c0HKGuGFHNnsrWC5NNFEMf1wKL2mzTFAVflS23oxYWhM4uE7+NlrJNYchqKzpOW1tHApXYwZa2T8HTop+rTOiVEhtf8vfXPYzi/oY/Ta6bsqHtQ7tzF74ReFqwxksTnxr+vFPQ6ZIMGMMdI/DgD8EB51tlUP3mx6JqJT2DuUn9h/MUZTHaSSkB7SyfZvhMlWa4/ZvBcccn/95pvDv2Dz34h4cZM=~-1~||-1||~-1; ak_bmsc=B8215182B0335F5E4C436BE27742CDD3~000000000000000000000000000000~YAAQAwUgF/+op1R8AQAAdec3Xg3w9ZxEF3UOrFdhf4mNix8sepWxcJtqoDryLMdQILgVjITRR8DZarmiIDIhQlfq9MUYj3K7mQZ+xJMCgfTY1ZqyfJ+cokyEw2qhn3uXxPD/CVYgQBsUum3s2B9zIDdUPYszQH3AuuOjhuN/eg5ZW4TvR5YpFmq0F2Vs6O50IKl5K3hJYN5EZmvcksKpp4kL35pQ43HRVzDnvaoWbIqixaPgUxCPE+Sjam+WWsRjlNk/882ge4dWoCThcK7bzi51PNLEOmJ+HpvvZKKN0WShd8MudkaMbR/nuycJ3SUK12+uaamT/RiP1BidYtcxjW6ouPrAKEy7oAA6UyoR+6fYq/NNug37T/dIimf0fI7PjwHsYqz6ZAGsIQA5eNyFtF8Ey61WjmtB49ksSNuuLxYugS6Qz2u9wQz2WFtH+Q0ABwLPVDmIH50nV3yHdCfpvGCK9m8qa4VyNPK6v69AuWC4Dgq1I30dycgbKrJtiD4pnq4L; bm_sz=53BC6A7B0966CF12E439E308D3D2A09B~YAAQAwUgF4Wop1R8AQAAluI3Xg18mImvOdUacolt/7wnEezTolcG6+IHO9PosbGqHcEDwsX5p/gkn8MBbCaQGozeUQZ8HkD7q3ReuEcCQzJp1A/IzC9tkgrbTfvNxBInMFO1GB+BaqX6E3SJm0zyVbwECaOBHwGG69p8faK3EweEmR5RznkWhCfVeIZZRqwcqK+QcjRgFk+lNcWkIHiH8ZmC/9AMotPzZdEaGVciXrWfcCfBCums6K8up3SM2Zz7qmzxidHY7NDA7v7zOGhaGu4owXEVavrxkbGurpj57ETeJ2PrhE6E2+EO~3622201~4534338; rxVisitor=1633666082462S2JBUDSV78M5JT5OM2CVA1G96ODVURKE; dtPC=2$468297051_667h-vEHJVRMGCTIMMPMEDQNPVENEQLFKUCEUQ-0e0; AMCV_4353388057AC8D357F000101%40AdobeOrg=870038026%7CMCIDTS%7C18909%7CMCMID%7C69206571533136945192735822806822950674%7CMCAAMLH-1634273093%7C8%7CMCAAMB-1634273093%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1633675493s%7CNONE%7CvVersion%7C5.0.0; at_check=true; mbox=session#2e4fa5eab5524626b39b76daeff7538d#1633670154|PC#2e4fa5eab5524626b39b76daeff7538d.36_0#1696913095; INGRESSCOOKIE=1633668294.545.19204.813475; w-rctx=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE2MzM2NjgyOTMsImV4cCI6MTYzMzY3MTg5MywiaWF0IjoxNjMzNjY4MjkzLCJpc3MiOiJXb29sd29ydGhzIiwiYXVkIjoid3d3Lndvb2x3b3J0aHMuY29tLmF1Iiwic2lkIjoiMCIsInVpZCI6ImVhYjk5ODNhLTA5ZWMtNGUwOC05NmVlLTcwYjkwNDM4ZDNhZCIsIm1haWQiOiIwIiwiYXV0IjoiU2hvcHBlciIsImF1YiI6IjAiLCJhdWJhIjoiMCIsIm1mYSI6IjEifQ.L84SQ3MQWWWVOlmcFQD-OpiJIduLoueXG886X-FjIvWORQz3-n6Z-DMaZIueznqY4Yhr9XAfzJrZDfFngBxmjrErmHzKDqMNdA00gaY0R7ZT2USpW07qGfgPHg7fEExw7oyyZRVNAzYUbtGQva0nF3GtypD0_FDB559l-B3WrqNDywHy5aWZUuJS5tIyVIlszIlcWhfubEguoCI508t5s3MBHQ4e02e6J4_ftnwI3QgfAeKc_WrJzO_kXqG0Am0KFEJ9H5au7rGdcNaPTUbrAocMRvTj5hBCJcIx4VTsSzMnA98hZX7ZMK5MXfqLgAAyCtVI95Sq5AU6aREa6LYhkQ; wow-auth-token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE2MzM2NjgyOTMsImV4cCI6MTYzMzY3MTg5MywiaWF0IjoxNjMzNjY4MjkzLCJpc3MiOiJXb29sd29ydGhzIiwiYXVkIjoid3d3Lndvb2x3b3J0aHMuY29tLmF1Iiwic2lkIjoiMCIsInVpZCI6ImVhYjk5ODNhLTA5ZWMtNGUwOC05NmVlLTcwYjkwNDM4ZDNhZCIsIm1haWQiOiIwIiwiYXV0IjoiU2hvcHBlciIsImF1YiI6IjAiLCJhdWJhIjoiMCIsIm1mYSI6IjEifQ.L84SQ3MQWWWVOlmcFQD-OpiJIduLoueXG886X-FjIvWORQz3-n6Z-DMaZIueznqY4Yhr9XAfzJrZDfFngBxmjrErmHzKDqMNdA00gaY0R7ZT2USpW07qGfgPHg7fEExw7oyyZRVNAzYUbtGQva0nF3GtypD0_FDB559l-B3WrqNDywHy5aWZUuJS5tIyVIlszIlcWhfubEguoCI508t5s3MBHQ4e02e6J4_ftnwI3QgfAeKc_WrJzO_kXqG0Am0KFEJ9H5au7rGdcNaPTUbrAocMRvTj5hBCJcIx4VTsSzMnA98hZX7ZMK5MXfqLgAAyCtVI95Sq5AU6aREa6LYhkQ; prodwow-auth-token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE2MzM2NjgyOTMsImV4cCI6MTYzMzY3MTg5MywiaWF0IjoxNjMzNjY4MjkzLCJpc3MiOiJXb29sd29ydGhzIiwiYXVkIjoid3d3Lndvb2x3b3J0aHMuY29tLmF1Iiwic2lkIjoiMCIsInVpZCI6ImVhYjk5ODNhLTA5ZWMtNGUwOC05NmVlLTcwYjkwNDM4ZDNhZCIsIm1haWQiOiIwIiwiYXV0IjoiU2hvcHBlciIsImF1YiI6IjAiLCJhdWJhIjoiMCIsIm1mYSI6IjEifQ.L84SQ3MQWWWVOlmcFQD-OpiJIduLoueXG886X-FjIvWORQz3-n6Z-DMaZIueznqY4Yhr9XAfzJrZDfFngBxmjrErmHzKDqMNdA00gaY0R7ZT2USpW07qGfgPHg7fEExw7oyyZRVNAzYUbtGQva0nF3GtypD0_FDB559l-B3WrqNDywHy5aWZUuJS5tIyVIlszIlcWhfubEguoCI508t5s3MBHQ4e02e6J4_ftnwI3QgfAeKc_WrJzO_kXqG0Am0KFEJ9H5au7rGdcNaPTUbrAocMRvTj5hBCJcIx4VTsSzMnA98hZX7ZMK5MXfqLgAAyCtVI95Sq5AU6aREa6LYhkQ; bm_sv=E0A3EBBAD80136CEFD1A30D22F7EBE6A~8AycaT7dzr2hsnlWx0Nu//lSF1ca2KzJ+Ra4OL7ZaWfD88j4QqHeEi53bMSmcPs32aeYQUBaQgPX29d+/YLELLNXuW67Fb2X/koKFjald9DjIl3yyxeZsiWyA0ON3b613lD8e34LQPSlqtO6MZ8FKCM7hFZcQ6csc8XyQ+wFkKc=; dtLatC=13; bm_mi=A92506C9405827470BCDB08C59284095~/oJslc6beUVhWTLVBSuMg4JsOILCYQgbrWSQjpdKiCjl4nG07MHfux3UVkNVPzobyNyrfmL+7zV1Fyugb6VnU4cAz2wWj/a7ThdjJIbQ9zVDyOLIS95g0H7EwgE0a5kAGBdIwuneWeKo/Q8T/1K6tzkt+MpWf91LnlawAbhBhT3eGLDmfVexjU12dfDOQQ0IajOiv1A+v+MAfMMrPf+8F1ZDYr4+kQhxH+7bMl4nKqGiKYcbWgOiv14HIp6rQrdEpqLuvl789T6DYZ7yUlkMWA==; rxvt=1633670097208|1633668252965; ai_user=f3s4g1HEvoqo+ANNsBXesh|2021-10-08T04:44:53.630Z; ai_session=xcVehA8zcJnAsl2aGblVzb|1633668293789|1633668293789; AMCVS_4353388057AC8D357F000101%40AdobeOrg=1; mboxEdgeCluster=36',
    }

    s = get_session()
    # s.headers.update(OrderedDict(headers))
    print("reqs homepage")
    # get = s.get("https://www.woolworths.com.au/", timeout=5)
    # print(get.headers)

    get = s.get("https://shop.coles.com.au/search/resources/store/20601/productview/bySeoUrlKeyword/lime-mandarin-hand-wash", headers=headers, timeout=2, proxies={"http":"http://frenox:trenox@43.229.61.124:3128", "https":"https://frenox:trenox@43.229.61.124:3128"})
    print(get)
    # json_data = get.json()

    # product = json_data['product']
    # print(product)

    return {
        'statusCode': 200,
        # 'body': json.dumps(product)
    }

print(get_woolies({"woolies": "133211"}))