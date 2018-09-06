import requests


def get_auth_url():
    weibo_auth_url = 'https://api.weibo.com/oauth2/authorize'
    redirect_url = 'http://127.0.0.1:8000/complete/weibo/'
    auth_url = weibo_auth_url + '?client_id={client_id}&redirect_uri={re_url}'.format(client_id=2176707864, re_url=redirect_url)

    print(auth_url)


def get_access_token(code):
    access_token_url = 'https://api.weibo.com/oauth2/access_token'
    re_dict = requests.post(access_token_url, data={
                                               'client_id': 2176707864,
                                               'client_secret': 'b6cab58f5d4179eb4b1038a3f232fcce',
                                               'grant_type': 'authorization_code',
                                               'code': code,
                                               'redirect_uri': 'http://127.0.0.1:8000/complete/weibo/',
    })

    pass


if __name__ == '__main__':
    get_auth_url()
    get_access_token(code='fd021f8747e1995d1ecbe17b376964c3')
