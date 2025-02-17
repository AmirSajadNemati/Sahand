import json
import requests

api_key = '39eeadfb9773068680aa733a485f7098'
url = "https://api.msgway.com/send"


def send_sms_login(phone, code):
    headers = {
        "apiKey": api_key,
        "accept-language": "fa",
        "Content-Type": "application/json"
    }
    body = {
        "mobile": str(phone),
        "method": "sms",
        "code": str(code),
        "templateID": 3157,
        # "params": [
        #     "راه پیام",
        #     "msgway.com"
        # ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))

def send_sms_new_task(phone, sex, full_name, task, task_proj):
    headers = {
        "apiKey": api_key,
        "accept-language": "fa",
        "Content-Type": "application/json"
    }
    body = {
        "mobile": str(phone),
        "method": "sms",
        "templateID": 13398,
        "params": [
            sex,
            full_name,
            task,
            task_proj
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))

def send_sms_author(phone, course, episode, user):
    headers = {
        "apiKey": api_key,
        "accept-language": "fa",
        "Content-Type": "application/json"
    }
    body = {
        "mobile": str(phone),
        "method": "sms",
        "templateID": 13469,
        "params": [
            course,
            episode,
            user
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))

def send_sms_user(phone, user, course, episode):
    headers = {
        "apiKey": api_key,
        "accept-language": "fa",
        "Content-Type": "application/json"
    }
    body = {
        "mobile": str(phone),
        "method": "sms",
        "templateID": 13470,
        "params": [
            user,
            course,
            episode,
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))