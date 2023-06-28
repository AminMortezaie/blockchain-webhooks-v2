from trc20webhook.services.utils import get_wallet, get_network, get_coin, get_block
from rest_framework import status
from trc20webhook.models import TransactionHistory, Wallet, Network, Coin, Block
from trc20webhook.services.get_blocks_operators import get_request_response, get_int_number_from_hex
from trc20webhook.services.get_blocks_links import link_provider, payload
from trc20webhook.services.wallets_hashmap import WalletsHashMap


def create_transaction(
        tx_hash: str,
        amount: int,
        coin: Coin,
        wallet: Wallet,
        network: Network,
        tx_type: str) -> TransactionHistory:

    tx_type = 'deposit' if tx_type == 'incoming' else 'withdrawal'
    transaction = TransactionHistory.objects.create(transaction_hash=tx_hash, amount=amount,
                                                    coin=coin, network=network, wallet=wallet,
                                                    transaction_type=tx_type)
    return transaction


def get_last_block_num_from_db(network: Network):
    block_obj = get_block(network=network)
    return block_obj.last_block_number


def get_last_block_num_from_getblock(network: Network):
    network_name = network.name
    key = network_name + "last-block-num"

    url = link_provider[key]
    payload_data = payload[key]

    hex_result = get_request_response(url, payload=payload_data)['result']
    return get_int_number_from_hex(hex_result)


def get_blocks(network: Network) -> dict:
    network_name = network.name
    key = network_name + "start-to-end"
    url = link_provider[key]

    start_number = get_last_block_num_from_db(network)
    end_number = get_last_block_num_from_getblock(network)

    payload_data = payload[key]
    payload_data['startNum'] = start_number
    payload_data['endNum'] = end_number

    blocks_data = get_request_response(url, payload_data)

    return blocks_data





