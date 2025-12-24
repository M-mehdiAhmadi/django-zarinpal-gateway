import json
import requests
from django.conf import settings
from django.http import HttpRequest

class Zarinpal:
    def __init__(self, request: HttpRequest, amount, description, mobile=None, email=None) -> None:
        self.merchant_id = settings.ZARINPAL_MERCHANT_ID
        self.amount = amount
        self.description = description
        self.callback_url = request.build_absolute_uri(settings.ZARINPAL_CALLBACK_URL)
        self.mobile = mobile
        self.email = email

    # -----------------------------
    # Payment Request
    # -----------------------------
    def send_request(self) -> dict:
        return self._post(
            settings.ZARINPAL_API_REQUEST_URL,
            self._build_request_payload()
        )

    def _build_request_payload(self) -> dict:
        payload = {
            "merchant_id": self.merchant_id,
            "amount": self.amount,
            "description": self.description,
            "callback_url": self.callback_url,
            "metadata": {}
        }
        if self.mobile:
            payload["metadata"]["mobile"] = self.mobile
        if self.email:
            payload["metadata"]["email"] = self.email
        return payload

    # -----------------------------
    # Payment Verify
    # -----------------------------
    def verify(self, authority) -> dict:
        payload = {
            "merchant_id": self.merchant_id,
            "amount": self.amount,
            "authority": authority
        }
        return self._post(settings.ZARINPAL_API_VERIFY_URL, payload)
    
    # -----------------------------
    # Generic POST helper
    # -----------------------------
    def _post(self, url, payload) -> dict:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        try:
            response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e),"response":json.dump(obj=response.json(),indent=4)}

