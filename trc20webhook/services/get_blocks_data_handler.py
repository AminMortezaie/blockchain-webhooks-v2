from abc import abstractmethod
from trc20webhook.models import Network


# wallets_hashmap
# { (address:network) : True }


# if get_block_wallet = wallets_hashmap[]
# get_wallet()

class BlocksDataHandler:

    @abstractmethod
    def get_blocks_wallets_data(self) -> dict: ...

    def check_is_exist_wallet(self) -> bool:
        pass

    def extract_data_for_our_wallet(self) -> dict:
        pass

    # it's necessary to add status to our temporary table
    def add_transaction_to_waiting_queue(self):
        pass

    def create_transaction(self):
        pass
