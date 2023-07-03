from webhook.services.singleton_pattern import SingletonMeta
from trc20webhook.services.get_blocks_operators import add_value_to_dict_values_by_key


class DataHashMap(metaclass=SingletonMeta):
    _wallets_hashmap = {}
    _waiting_tx_queue = {}

    @property
    def wallets_hashmap(self):
        return self._wallets_hashmap

    @wallets_hashmap.setter
    def wallets_hashmap(self, new_wallets_hashmap):
        self._wallets_hashmap = new_wallets_hashmap

    @property
    def waiting_tx_queue(self):
        return self._waiting_tx_queue

    @waiting_tx_queue.setter
    def waiting_tx_queue(self, new_waiting_queue):
        self._waiting_tx_queue = new_waiting_queue

    def waiting_tx_queue_setter_by_value(self, key, value):
        add_value_to_dict_values_by_key(key, self._waiting_tx_queue, value)
