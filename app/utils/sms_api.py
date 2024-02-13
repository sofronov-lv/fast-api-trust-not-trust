import json
import requests

from app.core.config import IQ_SMS_LOGIN, IQ_SMS_PASSWORD


class IQSms:
    """class for using iqsms.ru service via JSON interface"""
    __host = "json.gate.iqsms.ru"

    def __init__(self):
        self.login = IQ_SMS_LOGIN
        self.password = IQ_SMS_PASSWORD

    def send_request(self, uri, params: dict):
        url = self.get_url(uri)
        data = self.form_packet(params)
        try:
            return requests.post(url, data=data, verify=False)

        except Exception as err:
            return err

    def get_url(self, uri):
        return f"https://{self.get_host()}/{uri}/"

    def form_packet(self, params: dict):
        params["login"] = self.login
        params["password"] = self.password
        params["statusQueueName"] = None
        params["scheduleTime"] = None
        packet = json.dumps(params)

        return packet

    def get_host(self):
        """Return current requests host """
        return self.__host

    def set_host(self, host):
        """Changing default requests host """
        self.__host = host

    def send(self, messages):
        """Sending sms packet"""
        return self.send_request("send", params={"messages": messages})

    def status(self, messages):
        """Retrieve sms statuses packet by its ids """
        params = {"messages": messages}
        return self.send_request("status", params)

    def status_queue(self, limit=5):
        """Retrieve latest statuses from queue """
        params = {"statusQueueName": None, "statusQueueLimit": limit}
        return self.send_request("statusQueue", params)

    def credits(self):
        """Retrieve current credit balance """
        return self.send_request("credits", params={})

    def senders(self):
        """Retrieve available signs """
        return self.send_request("senders", params={})


iq_sms = IQSms()


def send_sms(phone_number: str, code: str, id_: int):
    """Sending sms packet"""
    message = {
        "clientId": str(id_),
        "phone": phone_number,
        "text": code,
        "sender": "Trust"
    }
    if not (response := iq_sms.send(message)):
        return False

    result = eval(response.text)
    return True if result["messages"][0]["status"] == "accepted" else False
