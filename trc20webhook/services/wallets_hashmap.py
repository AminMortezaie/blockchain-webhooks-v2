from webhook.services.singleton_pattern import SingletonMeta


class WalletsHashMap(object, metaclass=SingletonMeta):
    _wallets_hashmap = {}

    @property
    def wallets_hashmap(self):
        return self._wallets_hashmap

    @wallets_hashmap.setter
    def wallets_hashmap(self, new_wallets_hashmap):
        if self.wallets_hashmap != new_wallets_hashmap:
            self._wallets_hashmap = new_wallets_hashmap
        else:
            print("wallet is the latest version no need to update")



