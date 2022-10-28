from algosdk import account, mnemonic


class Account:
    def __init__(self):
        self._private_key, _ = account.generate_account()

    def get_mnemonic(self):
        return mnemonic.from_private_key(self._private_key)
