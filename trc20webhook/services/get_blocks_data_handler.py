from trc20webhook.services.utils import check_contract_address_is_valid, create_transaction
from trc20webhook.services.get_blocks_operators import convert_hex_number_to_int, add_value_to_dict_values_by_key
from trc20webhook.services.get_blocks_data_extractor import get_confirmation_state
from trc20webhook.services.data_hashmap import DataHashMap
import json
from abc import abstractmethod
import base58

_wallets = {'TAmSperixPEYyEVozADE6unuKuK44QSood_trc20': True, 'TF4szfVCVQCC62L7G4M5yMA2nBRTGNko1r_trc20': True,
            'TWSTYpRKBzSZggfcesAQDJv6o2RMgVAvfi_trc20': True, 'TPqRH6aUK7t4aCtky2Y1pe7qkU7oWCYwSL_trc20': True,
            'TUAZKEekUaRfyQ1HmunwQcDnBUJkYV1yrs_trc20': True}


class BlocksDataHandler:

    data_hashmap_obj = DataHashMap()

    @abstractmethod
    def get_blocks_wallets_data(self, blocks_data) -> dict: ...

    @abstractmethod
    def _tx_wrapper(self, tx_id, tx, type_, timestamp) -> dict: ...

    @staticmethod
    def check_is_exist_wallet(network_symbol: str, wallets_hashmap: dict, get_block_wallets_data: dict) -> list:
        our_wallets_list = []
        for key, value in get_block_wallets_data.items():
            key = key + "_" + network_symbol
            if key in wallets_hashmap:
                our_wallets_list.append(key)
        return our_wallets_list

    def add_transaction_to_waiting_queue(self, network_symbol: str, our_wallets_list: list, get_block_wallets_data: dict):
        for wallet in our_wallets_list:
            wallet = wallet.split("_")[0]
            data = get_block_wallets_data[wallet]
            for tx in data:
                tx_id = tx[0]
                sender_address = tx[1]
                contract_address = tx[4]
                state_ = check_contract_address_is_valid(network_symbol=network_symbol,
                                                         contract_address=contract_address)

                if sender_address == wallet:
                    tx_type = 'withdrawal'
                else:
                    tx_type = 'deposit'

                if state_:
                    key = tx_id + "_" + network_symbol
                    tx.append(tx_type)
                    self.data_hashmap_obj.waiting_tx_queue_setter_by_value(key, tx)
        # print(self.data_hashmap_obj.waiting_tx_queue)

    @abstractmethod
    def check_for_confirmed_txs(self, waiting_queue_txs): ...

    @staticmethod
    def create_transaction(self):
        pass


class TRONDataHandler(BlocksDataHandler):
    KNOWN_SMART_CONTRACTS_TX_DATA_LEN = 128 + 8
    UNKNOWN_SMART_CONTRACTS_TX_DATA_LEN = 192 + 8
    _symbol = "trc20"
    _temp_get_block_wallets_data = {}

    @staticmethod
    def _convert_hex_to_base58_address(eth_address):
        return base58.b58encode_check(bytes.fromhex(eth_address)).decode()

    def _wrap_inside_contract_data(self, tx):
        data = tx['data']
        try:
            if len(data) == self.KNOWN_SMART_CONTRACTS_TX_DATA_LEN:
                sender_address = self._convert_hex_to_base58_address(tx['owner_address'])
                receiver_address = self._convert_hex_to_base58_address("41" + data[32:72])
                amount = convert_hex_number_to_int(data[96:])
                return sender_address, receiver_address, amount

            elif len(data) == self.UNKNOWN_SMART_CONTRACTS_TX_DATA_LEN:
                sender_address = self._convert_hex_to_base58_address("41" + data[32:72])
                receiver_address = self._convert_hex_to_base58_address("41" + data[96:136])
                amount = convert_hex_number_to_int(data[136:])
                return sender_address, receiver_address, amount
        except Exception as e:
            print(e)

    def _tx_wrapper(self, tx_id, tx, type_, timestamp):
        match type_:
            # This is pure TRX transfer
            case "TransferContract":
                contract_address = ""
                amount = tx['amount']
                sender_address = self._convert_hex_to_base58_address(tx['owner_address'])
                receiver_address = self._convert_hex_to_base58_address(tx['to_address'])
                return [tx_id, sender_address, receiver_address, amount, contract_address, timestamp]

            case "TriggerSmartContract":
                contract_address = self._convert_hex_to_base58_address(tx['contract_address'])
                try:
                    sender_address, receiver_address, amount = self._wrap_inside_contract_data(tx)
                    return [tx_id, sender_address, receiver_address, amount, contract_address, timestamp]
                except:
                    pass

            # todo Trc10 transactions case "TransferAssetContract"
            case _:
                pass

    def get_blocks_wallets_data(self, blocks_data) -> dict:
        for block_data in blocks_data['block']:
            block_timestamp = int(int(block_data['block_header']['raw_data']['timestamp']) / pow(10, 3))
            for tx in block_data['transactions']:
                type_ = tx['raw_data']['contract'][0]['type']
                transaction = tx['raw_data']['contract'][0]['parameter']['value']
                tx_id = tx['txID']
                if self._tx_wrapper(tx_id, transaction, type_, block_timestamp):
                    tx_data = self._tx_wrapper(tx_id, transaction, type_, block_timestamp)
                    sender_address = tx_data[1]
                    receiver_address = tx_data[2]
                    add_value_to_dict_values_by_key(sender_address, self._temp_get_block_wallets_data, tx_data)
                    add_value_to_dict_values_by_key(receiver_address, self._temp_get_block_wallets_data, tx_data)

        return self._temp_get_block_wallets_data

    def check_for_confirmed_txs(self, waiting_queue_txs: dict):
        for key, value in waiting_queue_txs.items():
            tx_hash = key.split("_")[0]
            print(get_confirmation_state(network_symbol=self._symbol, tx_hash=tx_hash)['confirmed'])
            if get_confirmation_state(network_symbol=self._symbol, tx_hash=tx_hash)['confirmed']:
                tx_hash = value[0][0]
                tx_type = value[0][6]

                if tx_type == "withdrawal":
                    wallet_address = value[0][1]
                else:
                    wallet_address = value[0][2]

                print(wallet_address)

                amount = value[0][3]
                print(amount)
                contract_address = value[0][4]
                timestamp = value[0][5]

                create_transaction(network_symbol=self._symbol, wallet_address=wallet_address,
                                   tx_hash=tx_hash, amount=amount, contract_address=contract_address,
                                   timestamp=timestamp, tx_type=tx_type)
                # waiting_queue_txs.pop(key)




f = open("test.json")
blocks_dat = json.load(f)

obj = TRONDataHandler()
wallets_lst = obj.get_blocks_wallets_data(blocks_dat)
our_wallets_lst = obj.check_is_exist_wallet(network_symbol="trc20", wallets_hashmap=_wallets, get_block_wallets_data=wallets_lst)
obj.add_transaction_to_waiting_queue("trc20", our_wallets_lst, wallets_lst)
test = obj.data_hashmap_obj
obj.check_for_confirmed_txs(waiting_queue_txs=test.waiting_tx_queue)


