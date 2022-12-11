import environ
import requests

env = environ.Env()
environ.Env.read_env()


def notify_client(message_id, text, phone):
    url = f'https://probe.fbrq.cloud/v1/send/{message_id}'
    headers = {'authorization': 'Bearer ' + env('JWT')}
    return requests.post(url, json={'id': message_id,
                                    'phone': phone,
                                    'text': text},
                         headers=headers)
