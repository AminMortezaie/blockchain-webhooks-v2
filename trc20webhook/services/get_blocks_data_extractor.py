from webhook.services.utils import get_request_response, \
    convert_hex_number_to_int, post_request_response

from trc20webhook.services.model_utils import get_last_block_num_from_db
from trc20webhook.models import Network
from trc20webhook.services.get_blocks_links import link_provider, payload
from trc20webhook.services.data_hashmap import DataHashMap

data_hashmap_obj = DataHashMap()


def get_last_block_num_from_getblock(network: Network):
    network_name = network.symbol
    key = network_name + "-last-block-num"

    url = link_provider[key]
    payload_data = payload[key]

    hex_result = post_request_response(url, payload=payload_data)['result']
    return convert_hex_number_to_int(hex_result)


def get_blocks_(network: Network) -> tuple:
    network_name = network.symbol
    key = network_name + "-start-to-end"
    url = link_provider[key]

    start_number = get_last_block_num_from_db(network)
    end_number = get_last_block_num_from_getblock(network)

    payload_data = payload[key]
    payload_data['startNum'] = start_number
    payload_data['endNum'] = end_number

    blocks_data = post_request_response(url, payload_data)
    # todo shahab bad pattern!!!
    for block_data in blocks_data['block']:
        block_number = block_data['block_header']['raw_data']['number']
        print('data to add ::: block_number:::', block_number)
        data_hashmap_obj.tron_blocks_data_setter_by_value(block_number, block_data)
    print("tron block data :::")
    print(data_hashmap_obj.tron_blocks_data.keys())
    # for key, value in data_hashmap_obj.tron_blocks_data.items():
    #     print(key)

    return blocks_data, end_number


def get_confirmation_state(network_symbol: str, tx_hash: str) -> dict:
    key = network_symbol + "-check-confirmation"
    url = link_provider[key]
    url = url + tx_hash
    tx_data = get_request_response(url)
    return tx_data









