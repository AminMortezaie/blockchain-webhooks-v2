import json
from abc import abstractmethod
import base58


class BlocksDataHandler:

    @abstractmethod
    def get_blocks_wallets_data(self, blocks_data) -> dict: ...

    @abstractmethod
    def _tx_wrapper(self, tx, type_) -> dict: ...

    def check_is_exist_wallet(self) -> bool:
        pass

    def extract_data_for_our_wallet(self) -> dict:
        pass

    # it's necessary to add status to our temporary table
    def add_transaction_to_waiting_queue(self):
        pass

    def create_transaction(self):
        pass


class TRONDataHandler(BlocksDataHandler):
    KNOWN_SMART_CONTRACTS_TX_DATA_LEN = 136
    UNKNOWN_SMART_CONTRACTS_TX_DATA_LEN = 200
    _types = {}

    @staticmethod
    def _convert_hex_to_base58_address(eth_address):
        return base58.b58encode_check(bytes.fromhex(eth_address)).decode()

    @staticmethod
    def _convert_hex_number_to_int(hex_number):
        return int(hex_number, 16)

    def _wrap_inside_contract_data(self, tx):
        data = tx['data']
        if len(data) == self.KNOWN_SMART_CONTRACTS_TX_DATA_LEN:
            sender_address = self._convert_hex_to_base58_address(tx['owner_address'])
            receiver_address = self._convert_hex_to_base58_address("41" + data[32:72])
            amount = self._convert_hex_number_to_int(data[96:])
            return sender_address, receiver_address, amount

        elif len(data) == self.UNKNOWN_SMART_CONTRACTS_TX_DATA_LEN:
            sender_address = self._convert_hex_to_base58_address("41" + data[32:72])
            receiver_address = self._convert_hex_to_base58_address("41" + data[96:136])
            amount = self._convert_hex_number_to_int(data[136:])
            return sender_address, receiver_address, amount

    def _tx_wrapper(self, tx, type_):
        match type_:
            # This is pure TRX transfer
            case "TransferContract":
                contract_address = ""
                amount = tx['amount']
                sender_address = tx['owner_address']
                receiver_address = tx['to_address']
                return sender_address, receiver_address, amount, contract_address

            case "TriggerSmartContract":
                contract_address = self._convert_hex_to_base58_address(tx['contract_address'])
                data = tx['data']
                sender_address, receiver_address, amount = self._wrap_inside_contract_data(tx)
                return sender_address, receiver_address, amount, contract_address

            # Trc10 transactions
            case "TransferAssetContract":
                pass

    def get_blocks_wallets_data(self, blocks_data) -> dict:
        for block_data in blocks_data['block']:
            for tx in block_data['transactions']:
                type_ = tx['raw_data']['contract'][0]['type']
                transaction = tx['raw_data']['contract'][0]['parameter']['value']
                self._tx_wrapper(transaction, type_)


f = open("./test1.json")
blocks_dat = json.load(f)

obj = TRONDataHandler().get_blocks_wallets_data(blocks_dat)
