import json
import time
from eth_account.messages import encode_defunct
from eth_account import Account

def generate_qr_payload(private_key, wallet_address):
    timestamp = int(time.time())

    message = f"{wallet_address}:{timestamp}"
    msg = encode_defunct(text=message)

    signed_message = Account.sign_message(msg, private_key=private_key)

    qr_data = {
        "wallet": wallet_address,
        "timestamp": timestamp,
        "signature": signed_message.signature.hex()
    }

    return qr_data


def validate_qr(qr_data):
    wallet = qr_data["wallet"]
    timestamp = qr_data["timestamp"]
    signature = qr_data["signature"]

    message = f"{wallet}:{timestamp}"
    msg = encode_defunct(text=message)

    recovered = Account.recover_message(msg, signature=signature)

    if recovered.lower() != wallet.lower():
        return {"valid": False}

    if int(time.time()) - timestamp > 60:
        return {"valid": False, "reason": "Expired"}

    return {"valid": True}