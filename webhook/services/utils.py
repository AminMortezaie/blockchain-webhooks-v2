import datetime
import requests
from django.conf import settings
from rest_framework import status


GETBLOCK_API = settings.GETBLOCK_API
HEADERS = {
    "x-api-key": GETBLOCK_API,
    "Content-Type": "application/json",
}


def post_request_response(endpoint: str, payload: dict = None) -> dict:
    response = requests.post(endpoint, json=payload, headers=HEADERS, timeout=300)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print('API request failed with status code', response.status_code)


def get_request_response(endpoint: str):
    response = requests.get(endpoint)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print('API request failed with status code', response.status_code)


def convert_timestamp(timestamp: str) -> datetime:
    timestamp = int(timestamp)
    try:
        return datetime.datetime.fromtimestamp(timestamp) + datetime.timedelta(hours=3, minutes=30)
    except ValueError as error:
        print(f'error in converting timestamp...{timestamp}...{error}')
        return datetime.datetime.fromtimestamp(timestamp / 1000) + datetime.timedelta(hours=3, minutes=30)


def convert_hex_number_to_int(hex_number: str) -> int:
    return int(hex_number, 16)


def add_value_to_dict_values_by_key(key: str, hashmap: dict, value: str | list | dict) -> None:
    values = hashmap.get(key, [])
    values.append(value)
    hashmap[key] = values


def return_tx_type(sender_address: str, wallet_address: str):
    tx_type = 'withdrawal' if sender_address == wallet_address else 'deposit'
    return tx_type


def del_pair_from_dict_by_key(removable_lst: list, hashmap: dict) -> None:
    for removable_key in removable_lst:
        del hashmap[removable_key]
