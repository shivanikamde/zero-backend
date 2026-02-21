import hashlib
from eth_account import Account
from .contracts import w3, identity_contract, credential_contract, reputation_contract, ACCOUNT

def register_user(aadhaar_hash, is_kyc, is_above18, has_phone):

    # Create new wallet
    new_account = Account.create()
    wallet_address = new_account.address
    private_key = new_account.key.hex()

    # Commitment hash
    commitment = hashlib.sha256(aadhaar_hash.encode()).hexdigest()

    nonce = w3.eth.get_transaction_count(ACCOUNT.address)

    tx = identity_contract.functions.registerIdentity(
        wallet_address,
        commitment
    ).build_transaction({
        "from": ACCOUNT.address,
        "nonce": nonce,
        "gas": 3000000,
        "gasPrice": w3.to_wei("20", "gwei")
    })

    signed_tx = ACCOUNT.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)

    return {
        "wallet_address": wallet_address,
        "private_key": private_key,
        "commitment": commitment
    }