from trc20webhook.models import Wallet, Network, Coin, Block


def _get_wallet(wallet_address: str, network: Network, eth_address: str) -> Wallet | None:
    if network.symbol == "trc20":
        wallet_obj = Wallet.objects.get(network=network, eth_address=eth_address)
    else:
        wallet_obj = Wallet.objects.get(address=wallet_address, network=network)

    return wallet_obj


def get_wallet(wallet_address: str, network: Network, eth_address: str) -> Wallet | None:
    try:
        wallet_obj = _get_wallet(wallet_address, network, eth_address)
        return wallet_obj
    except Wallet.DoesNotExist:
        pass


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
        pass


def get_block(network: Network) -> Block | None:
    try:
        block_obj = Block.objects.get(network=network)
        return block_obj
    except Block.DoesNotExist:
        raise "There is no block for this network."


def check_contract_address_is_valid(contract_address: str, network_symbol: str):
    network = get_network(network_symbol)
    if Coin.objects.get(network=network, contract_address=contract_address):
        return True
    else:
        return False
