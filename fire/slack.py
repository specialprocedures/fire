import requests
import os
import json


class Grovetender:
    def __init__(self, url=None) -> None:
        if not url:
            self.webhook_url = os.environ["GROVE_URL"]
        else:
            self.webhook_url = url

        self.default_headers = {"Content-Type": "application/json"}

    def notify(self, text: str, data=None, headers=None):
        if not data:
            data = {}
            data["text"] = text
        if not headers:
            headers = self.default_headers

        r = requests.post(self.webhook_url, data=json.dumps(data), headers=headers)
