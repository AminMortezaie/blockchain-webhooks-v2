from trc20webhook.services.utils import get_wallet, get_network, get_coin, get_block
from rest_framework import status
from trc20webhook.models import TransactionHistory, Wallet, Network, Coin, Block
from trc20webhook.services.get_blocks_operators import get_request_response, \
    convert_hex_number_to_int, post_request_response
from trc20webhook.services.get_blocks_links import link_provider, payload


def get_last_block_num_from_db(network: Network):
    block_obj = get_block(network=network)
    return block_obj.last_block_number


def get_last_block_num_from_getblock(network: Network):
    network_name = network.symbol
    key = network_name + "-last-block-num"

    url = link_provider[key]
    payload_data = payload[key]

    hex_result = post_request_response(url, payload=payload_data)['result']
    return convert_hex_number_to_int(hex_result)


def get_blocks(network: Network) -> dict:
    network_name = network.symbol
    key = network_name + "-start-to-end"
    url = link_provider[key]

    start_number = get_last_block_num_from_db(network)
    end_number = get_last_block_num_from_getblock(network)

    payload_data = payload[key]
    payload_data['startNum'] = start_number
    payload_data['endNum'] = end_number

    blocks_data = post_request_response(url, payload_data)

    return blocks_data


def get_confirmation_state(network_symbol: str, tx_hash: str) -> dict:
    key = network_symbol + "-check-confirmation"
    url = link_provider[key]
    url = url + tx_hash
    tx_data = get_request_response(url)
    return tx_data









