from webhook.services.singleton_pattern import SingletonMeta


class DataHashMap(metaclass=SingletonMeta):
    _wallets_hashmap = {}
    _get_block_wallets_data = {}
    _waiting_tx_queue = {}

    @property
    def get_block_wallets_data(self):
        return self._get_block_wallets_data

    @get_block_wallets_data.setter
    def get_block_wallets_data(self, new_get_block_wallets_data):
        self._get_block_wallets_data = new_get_block_wallets_data

    @property
    def wallets_hashmap(self):
        return self._wallets_hashmap

    @wallets_hashmap.setter
    def wallets_hashmap(self, new_wallets_hashmap):
        self._wallets_hashmap = new_wallets_hashmap

    @property
    def waiting_tx_queue(self):
        return self._wallets_hashmap

    @waiting_tx_queue.setter
    def waiting_tx_queue(self, new_waiting_tx_queue):
        self._waiting_tx_queue = new_waiting_tx_queue

