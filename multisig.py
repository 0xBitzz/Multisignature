import json
from accounts import Account
from algosdk import encoding, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import Multisig, MultisigTransaction, PaymentTxn, wait_for_confirmation


def multi_sig_txn():
    # Create algod client
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    algod_address = "http://localhost:4001"
    algod_client = algod.AlgodClient(algod_token, algod_address)
    
    # Create multisig address
    passphrase1 = Account().get_mnemonic()
    account1 = mnemonic.to_public_key(passphrase1)
    
    passphrase2 = Account().get_mnemonic()
    account2 = mnemonic.to_public_key(passphrase2)

    passphrase3 = Account().get_mnemonic()
    account3 = mnemonic.to_public_key(passphrase3)

    msig = Multisig(version=1, threshold=2, addresses=[account1, account2, account3])
    input(f"Go to https://app.dappflow.org/dispenser to fund this account {msig.address()}, and hit enter")

    # Build transaction
    params = algod_client.suggested_params()

    # Send 1A from multisig address to account1
    amount = 1000000
    sender = msig.address()
    receiver = account1
    note = f"Sent 1A from {msig.address()} to {account1}".encode()
    txn = PaymentTxn(sender, params, receiver, amount, None, note)

    # Create a multisig transaction object to enable signing from threshold accounts
    mtx = MultisigTransaction(txn, msig)
    mtx.sign(mnemonic.to_private_key(passphrase1))
    mtx.sign(mnemonic.to_private_key(passphrase2))

    # Confirm txn
    try:
        txid = algod_client.send_raw_transaction(encoding.msgpack_encode(mtx))
        confirmed_txn = wait_for_confirmation(algod_client, txid, 6)
        print(f"Transaction confirmed in {confirmed_txn['confirmed-round']} rounds")
        print(f"Transaction information {json.dumps(confirmed_txn, indent=4)}")
    except Exception as err:
        print(err)
    

multi_sig_txn()
