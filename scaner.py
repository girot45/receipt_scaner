import json
from config import HOST, DEVICE_OS, CLIENT_VERSION, DEVICE_ID, ACCEPT, \
    USER_AGENT, ACCEPT_LANGUAGE, CLIENT_SECRET, OS, PHONE
import requests


class NalogRuPython:

    def __init__(self):
        self.__code = None
        self.__refresh_token = None
        self.__session_id = None
        self.set_session_id()

    def set_session_id(self) -> None:
        """
        Authorization using phone and SMS code
        """
        # self.__phone = str(input('Input phone in +70000000000
        # format: '))

        url = f'https://{HOST}/v2/auth/phone/request'
        payload = {
            'phone': PHONE,
            'client_secret': CLIENT_SECRET,
            'os': OS
        }
        headers = {
            'Host': HOST,
            'Accept': ACCEPT,
            'Device-OS': DEVICE_OS,
            'Device-Id': DEVICE_ID,
            'clientVersion': CLIENT_VERSION,
            'Accept-Language': ACCEPT_LANGUAGE,
            'User-Agent': USER_AGENT,
        }

        resp = requests.post(url, json=payload, headers=headers)

        self.__code = input('Input code from SMS: ')

        url = f'https://{HOST}/v2/auth/phone/verify'
        payload = {
            'phone': PHONE,
            'client_secret': CLIENT_SECRET,
            'code': self.__code,
            "os": OS
        }

        resp = requests.post(url, json=payload, headers=headers)

        self.__session_id = resp.json()['sessionId']
        self.__refresh_token = resp.json()['refresh_token']

    def refresh_token_function(self) -> None:
        url = f'https://{HOST}/v2/mobile/users/refresh'
        payload = {
            'refresh_token': self.__refresh_token,
            'client_secret': CLIENT_SECRET
        }

        headers = {
            'Host': HOST,
            'Accept': ACCEPT,
            'Device-OS': DEVICE_OS,
            'Device-Id': DEVICE_ID,
            'clientVersion': CLIENT_VERSION,
            'Accept-Language': ACCEPT_LANGUAGE,
            'User-Agent': USER_AGENT,
        }

        resp = requests.post(url, json=payload, headers=headers)

        self.__session_id = resp.json()['sessionId']
        self.__refresh_token = resp.json()['refresh_token']

    def _get_ticket_id(self, qr: str) -> str:
        """
        Get ticker id by info from qr code
        :param qr: text from qr code. Example "t=20200727T174700&s=746.00&fn=9285000100206366&i=34929&fp=3951774668&n=1"
        :return: Ticket id. Example "5f3bc6b953d5cb4f4e43a06c"
        """
        url = f'https://{HOST}/v2/ticket'
        payload = {'qr': qr}
        headers = {
            'Host': HOST,
            'Accept': ACCEPT,
            'Device-OS': DEVICE_OS,
            'Device-Id': DEVICE_ID,
            'clientVersion': CLIENT_VERSION,
            'Accept-Language': ACCEPT_LANGUAGE,
            'sessionId': self.__session_id,
            'User-Agent': USER_AGENT,
        }

        resp = requests.post(url, json=payload, headers=headers)

        return resp.json()["id"]

    def get_ticket(self, qr: str) -> dict:
        """
        Get JSON ticket
        :param qr: text from qr code. Example "t=20200727T174700&s=746.00&fn=9285000100206366&i=34929&fp=3951774668&n=1"
        :return: JSON ticket
        """
        ticket_id = self._get_ticket_id(qr)
        url = f'https://{HOST}/v2/tickets/{ticket_id}'
        headers = {
            'Host': HOST,
            'sessionId': self.__session_id,
            'Device-OS': DEVICE_OS,
            'clientVersion': CLIENT_VERSION,
            'Device-Id': DEVICE_ID,
            'Accept': ACCEPT,
            'User-Agent': USER_AGENT,
            'Accept-Language': ACCEPT_LANGUAGE,
            'Content-Type': 'application/json'
        }

        resp = requests.get(url, headers=headers)

        return resp.json()


# if __name__ == '__main__':
#     client = NalogRuPython()
#     qr_code = "t=20200709T2008&s=7273.00&fn=9282440300688488&i=14186&fp=1460060363&n=1"
#     ticket = client.get_ticket(qr_code)
#     print(json.dumps(ticket, indent=4, ensure_ascii=False))
#
#     client.refresh_token_function()
#     qr_code = "t=20170606T1137&s=65.00&fn=9999078900005565&i=24&fp=3071844235&n=1"
#     ticket = client.get_ticket(qr_code)
#     print(json.dumps(ticket, indent=4, ensure_ascii=False))
