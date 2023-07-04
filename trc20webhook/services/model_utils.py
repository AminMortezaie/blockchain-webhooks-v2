from trc20webhook.models import Wallet, Network, Coin, Block, TransactionHistory
from datetime import datetime


def get_wallet(wallet_address: str, network: Network) -> Wallet | None:
    try:
        wallet_obj = Wallet.objects.get(address=wallet_address, network=network)
        return wallet_obj
    except Wallet.DoesNotExist:
        pass


def get_all_wallets():
    wallets_hashmap = {}
    wallets = Wallet.objects.all()
    for wallet in wallets:
        key = wallet.address + "_" + wallet.network.symbol
        wallets_hashmap[key] = True
    return wallets_hashmap


def get_network(network: str) -> Network | None:
    try:
        network_obj = Network.objects.get(symbol=network)
    except Network.DoesNotExist:
        try:
            network_obj = Network.objects.get(name=network.capitalize()).first()
        except Network.DoesNotExist:
            network_obj = None
    return network_obj


def get_coin(network: Network, contract_address: str) -> Coin | None:
    try:
        coin_obj = Coin.objects.get(network=network, contract_address=contract_address)
        return coin_obj
    except Coin.DoesNotExist:
        return None


def get_block(network: Network) -> Block | None:
    try:
        block_obj = Block.objects.get(network=network)
        return block_obj
    except Block.DoesNotExist:
        raise "There is no block for this network."


def get_last_block_num_from_db(network: Network):
    block_obj = get_block(network=network)
    return block_obj.last_block_number


def update_last_block_number(network: Network, last_block_number: str):
    block_obj = get_block(network=network)
    block_obj.last_block_number = last_block_number
    block_obj.save()


def check_contract_address_is_valid(contract_address: str, network_symbol: str):
    network = get_network(network_symbol)
    try:
        coin = get_coin(network, contract_address)
        if coin:
            return True
    except Coin.DoesNotExist:
        return False


def create_transaction(network_symbol: str, wallet_address: str, tx_hash: str, amount: str,
                       contract_address: str, timestamp: str, tx_type: str):
    network = get_network(network_symbol)
    coin = get_coin(network, contract_address)
    timestamp = datetime.fromtimestamp(int(timestamp))
    wallet = get_wallet(wallet_address=wallet_address, network=network)
    amount = float(amount) / float(pow(10, int(coin.decimals)))

    try:
        TransactionHistory.objects.create(transaction_hash=tx_hash, amount=amount,
                                          coin=coin, network=network, wallet=wallet,
                                          transaction_type=tx_type, timestamp=timestamp)
    except Exception as e:
        print(e)
