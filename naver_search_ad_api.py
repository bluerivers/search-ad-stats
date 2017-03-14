import time
import hmac
import hashlib
import base64
import requests


class API:

    def __init__(self, customer_id, license_key, secret_key):
        self.customer_id = customer_id
        self.license_key = license_key
        self.secret_key = str.encode(secret_key)

    def retrieve_relative_keyword_stats(self, hint_keywords):

        http_method = "GET"
        service_url = "/keywordstool"

        # 키워드 5개만 요청을 할 수 있음
        start = 0
        ret = []

        while start < len(hint_keywords):
            current_epoch_time = int(round(time.time() * 1000))
            signature_str = (str(current_epoch_time) + '.' + http_method + "." + service_url).encode('utf-8')
            signature = base64.b64encode(hmac.new(self.secret_key, signature_str, digestmod=hashlib.sha256).digest())

            headers = {
                'X-Timestamp': str(current_epoch_time),
                'X-API-KEY': self.license_key,
                'X-Customer': str(self.customer_id),
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
                raise Exception(response.content)

            response.encoding = 'utf-8'
            keyword_list = response.json()['keywordList']

            ret.extend(keyword_list)
            start += 5

        return ret
