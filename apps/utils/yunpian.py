import requests
import json


class YunPian(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self, code, mobile):
        # 要传递的参数
        params = {
            'apikey': self.api_key,
            'mobile': mobile,
            'text': '【好吃生鲜】您的验证码是{code}。如非本人操作，请忽略本短信'.format(code=code)
        }

        response = requests.post(self.single_send_url, data=params)
        return json.loads(response.text)

if __name__ == '__main__':
    yun_pian = YunPian('24c092303f716528a2f74a3cd7f3232d')
    yun_pian.send_sms('2018', '15335887511')
