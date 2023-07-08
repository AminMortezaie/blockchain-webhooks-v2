from celery import shared_task, Task
from trc20webhook.services.model_utils import get_all_wallets, get_network, update_last_block_number
from trc20webhook.services.data_hashmap import DataHashMap
from trc20webhook.services.get_blocks_data_extractor import get_blocks_, get_last_block_num_from_getblock
from trc20webhook.services.get_blocks_data_handler import TRONDataHandler
from django.db import transaction
from django.core.cache import cache


@shared_task(name="update_wallets_hashmap")
def update_wallets_hashmap():
    DataHashMap.wallets_hashmap = get_all_wallets()


@shared_task(name="get_blocks_trc20")
def get_blocks_trc20():
    network = get_network("trc20")
    blocks_data, last_block_number = get_blocks_(network)
    update_last_block_number(network=network, last_block_number=last_block_number)


@shared_task(name='tron_data_handler')
def tron_data_handler():
    TRONDataHandler()


