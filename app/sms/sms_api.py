import json
import requests

from app.configs.config import IQ_SMS_LOGIN, IQ_SMS_PASSWORD


class SMS:
    URL = f"https://json.gate.iqsms.ru/send/"

    @staticmethod
    def send_sms(phone_number: str, code: str, id_="0"):
        """Sending sms packet"""
        message = {
            "clientId": str(id_),
            "phone": phone_number,
            "text": code,
            "sender": "Trust"
        }
        params = {
            "messages": message,
            'statusQueueName': None,
            'scheduleTime': None,
            "login": IQ_SMS_LOGIN,
            "password": IQ_SMS_PASSWORD
        }
        try:
            response = requests.post(SMS.URL, data=json.dumps(params), verify=False).text
            return True if response else False

        except Exception:
            return False
