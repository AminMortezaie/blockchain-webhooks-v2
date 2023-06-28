import datetime
import requests
from django.conf import settings
from rest_framework import status


GETBLOCK_API = settings.GETBLOCK_API
HEADERS = {
    "x-api-key": GETBLOCK_API,
    "Content-Type": "application/json",
}


def get_request_response(endpoint: str, payload: dict = None) -> dict:
    response = requests.post(endpoint, json=payload, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print('API request failed with status code', response.status_code)


def convert_timestamp(timestamp: str) -> datetime:
    return datetime.date.fromtimestamp(int(timestamp))


def get_int_number_from_hex(hex_number: str) -> int:
    return int(hex_number, 16)







