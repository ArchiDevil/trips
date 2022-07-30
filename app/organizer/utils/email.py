import requests

from flask import current_app


def send_email(address: str, subject: str, body: str):
    headers = {
        'accept': 'application/json',
        'api-key': current_app.config['SENDINBLUE_API_KEY'],
    }
    json = {
        "sender": {
            "name": "NoReply",
            "email": "noreply@hikehub.ru"
        },
        "to": [
            {
                "email": address,
                "name": address
            }
        ],
        "subject": subject,
        "htmlContent": body
    }

    response = requests.post('https://api.sendinblue.com/v3/smtp/email',
                             headers=headers, json=json)

    if response.status_code != 201:
        raise RuntimeError(response.content.decode('utf-8'))
