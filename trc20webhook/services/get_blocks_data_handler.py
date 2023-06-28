from trc20webhook.models import Network


class BlocksDataHandler:

    def get_blocks_wallets(self) -> list[str]:
        pass

    def check_is_exist_wallet(self) -> bool:
        pass

    def extract_data_for_our_wallet(self):
        pass

    # it's necessary to add status to our temporary table
    def add_transaction_to_waiting_queue(self):
        pass

    def create_transaction(self):
        pass






