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


def convert_hex_number_to_int(hex_number: str) -> int:
    return int(hex_number, 16)


def add_value_to_dict_values_by_key(key: str, hashmap: dict, value: str | list | dict) -> None:
    values = hashmap.get(key, [])
    values.append(value)
    hashmap[key] = values







