import time
import hmac
import hashlib
import base64
import requests


def retrieve_relative_keyword_stats(hint_keywords):

    customer_id = 1109060
    license_key = "01000000002a0f8aa24bb59ce0515ade311add34d64b0565164c2d84b1ccfef437720585d5"
    secret_key = b'AQAAAAAqD4qiS7Wc4FFa3jEa3TTWEWhRjLiqursERWAzUtuSLg=='
    http_method = "GET"
    service_url = "/keywordstool"

    # 키워드 5개만 요청을 할 수 있음
    start = 0
    ret = []

    while start < len(hint_keywords):
        current_epoch_time = int(round(time.time() * 1000))
        signature_str = (str(current_epoch_time) + '.' + http_method + "." + service_url).encode('utf-8')
        signature = base64.b64encode(hmac.new(secret_key, signature_str, digestmod=hashlib.sha256).digest())

        headers = {
            'X-Timestamp': str(current_epoch_time),
            'X-API-KEY': license_key,
            'X-Customer': str(customer_id),
            'X-Signature': signature
        }

        query_param = {
            'hintKeywords': ",".join(hint_keywords[start:start + 5]),
            'showDetail': 1,
            'includeHintKeywords': 0
        }

        response = requests.get('https://api.naver.com' + service_url, headers=headers, params=query_param)

        if response.status_code != 200:
            # error!
            print('error occurs', response.status_code, response.content)
            start += 5
            continue

        response.encoding = 'utf-8'
        keyword_list = response.json()['keywordList']

        ret.extend(keyword_list)
        start += 5

    return ret
