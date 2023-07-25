from django.conf import settings
import requests
import json
import structlog

logger = structlog.get_logger(__name__)


class GlobelabsException(Exception):
    pass

class M360:
    @staticmethod
    def send(mobile: str, message: str):
        # if mobile == "" or message == "":
        #     raise GlobelabsException("Mobile and message not null")
        url = settings.M360_URL + settings.M360_PASSPHRASE
        headers = {"Content-Type": "application/json"}
        payload = {
            "outboundSMSMessageRequest": {
                "clientCorrelator": settings.M360_SHORTCODE,
                "senderAddress": "SARISUKI",
                "outboundSMSTextMessage": {"message": message},
                "address": mobile,
            }
        }

        response = requests.post(url, data=json.dumps(payload), headers=headers)
