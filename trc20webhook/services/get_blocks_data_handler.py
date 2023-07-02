from trc20webhook.services.utils import check_contract_address_is_valid
from trc20webhook.services.get_blocks_operators import convert_hex_number_to_int, add_value_to_dict_values_by_key
from trc20webhook.services.data_hashmap import DataHashMap
import json
from abc import abstractmethod
import base58

_wallets = {'TAmSperixPEYyEVozADE6unuKuK44QSood': True, 'TF4szfVCVQCC62L7G4M5yMA2nBRTGNko1r': True, 'TWSTYpRKBzSZggfcesAQDJv6o2RMgVAvfi': True, 'TPqRH6aUK7t4aCtky2Y1pe7qkU7oWCYwSL': True}


class BlocksDataHandler:

    @abstractmethod
    def get_blocks_wallets_data(self, blocks_data) -> dict: ...

    @abstractmethod
    def _tx_wrapper(self, tx_id, tx, type_, timestamp) -> dict: ...

    @staticmethod
    def check_is_exist_wallet(wallets_hashmap: dict, get_block_wallets_data: dict) -> list:
        our_wallets_list = []
        for key, value in get_block_wallets_data.items():
            if key in wallets_hashmap:
                our_wallets_list.append(key)
        return our_wallets_list

    @staticmethod
    def check_contract_address_by_db(self, network_symbol: str, our_wallets_list: list, get_block_wallets_data: dict):
        for wallet in our_wallets_list:
            data = get_block_wallets_data[wallet]
            for tx in data:
                tx_id = tx[0]
                contract_address = tx[4]

                state_ = check_contract_address_is_valid(network_symbol=network_symbol, contract_address=contract_address)
                if state_:
                    DataHashMap.waiting_tx_queue[tx_id] = 1
    def extract_data_for_our_wallet(self, our_wallets_list: list, get_block_wallets_data: dict) -> dict:
        pass



    # it's necessary to add status to our temporary table
    def add_transaction_to_waiting_queue(self):
        pass

    def create_transaction(self):
        pass


class TRONDataHandler(BlocksDataHandler):
    KNOWN_SMART_CONTRACTS_TX_DATA_LEN = 128 + 8
    UNKNOWN_SMART_CONTRACTS_TX_DATA_LEN = 192 + 8
    _wallets = {'TWYfzKTykLzsXg4BNRm89qUqCD8CVqy4N6': True, 'TUsRU3D3QBvZBN8qLeTsFMEiKDFxe5qk5c': True,
                'TWSTYpRKBzSZggfcesAQDJv6o2RMgVAvfi': True, 'TPqRH6aUK7t4aCtky2Y1pe7qkU7oWCYwSL': True}
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
                return tx_id, sender_address, receiver_address, amount, contract_address, timestamp

            case "TriggerSmartContract":
                contract_address = self._convert_hex_to_base58_address(tx['contract_address'])
                try:
                    sender_address, receiver_address, amount = self._wrap_inside_contract_data(tx)
                    return tx_id, sender_address, receiver_address, amount, contract_address, timestamp
                except:
                    pass

            # Trc10 transactions
            # case "TransferAssetContract":
            #     pass

            case _:
                pass

    def get_blocks_wallets_data(self, blocks_data) -> dict:
        for block_data in blocks_data['block']:
            block_timestamp = block_data['block_header']['raw_data']['timestamp']
            for tx in block_data['transactions']:
                type_ = tx['raw_data']['contract'][0]['type']
                transaction = tx['raw_data']['contract'][0]['parameter']['value']
                tx_id = tx['txID']
                if self._tx_wrapper(tx_id, transaction, type_, block_timestamp):
                    tx_data = (self._tx_wrapper(tx_id, transaction, type_, block_timestamp))
                    sender_address = tx_data[1]
                    receiver_address = tx_data[2]
                    add_value_to_dict_values_by_key(sender_address, self._temp_get_block_wallets_data, tx_data)
                    add_value_to_dict_values_by_key(receiver_address, self._temp_get_block_wallets_data, tx_data)

        return self._temp_get_block_wallets_data


f = open("test1.json")
blocks_dat = json.load(f)

obj = TRONDataHandler()
wallets_lst = obj.get_blocks_wallets_data(blocks_dat)
print(obj.check_is_exist_wallet(wallets_hashmap=_wallets, get_block_wallets_data=wallets_lst))


