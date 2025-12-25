import os
import json
import argparse
import pathlib
from web3 import Web3
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization


def add_model_to_blockchain(pem_file_path):
    load_dotenv()
    path_obj = pathlib.Path(pem_file_path)

    if not path_obj.exists():
        return f"Error: File {pem_file_path} not found", None

    model_name = path_obj.stem

    try:
        with open(pem_file_path, "rb") as f:
            pem_data = f.read()

        # Load the PEM file and convert to raw 32 bytes (Ed25519 standard)
        public_key_obj = serialization.load_pem_public_key(pem_data)
        raw_key_bytes = public_key_obj.public_bytes(
            encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
        )
    except Exception as e:
        return f"Error processing PEM file: {e}", None

    base_path = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_path, "deployed_info.json")

    if not os.path.exists(json_path):
        return f"Error: {json_path} not found", None

    # Setup Web3
    w3 = Web3(Web3.HTTPProvider(os.getenv("INFURA_URL")))
    private_key = os.getenv("PRIVATE_KEY")
    my_address = Web3.to_checksum_address(os.getenv("MY_ADDRESS"))

    with open(json_path, "r") as f:
        data = json.load(f)
        contract = w3.eth.contract(address=data["address"], abi=data["abi"])

    try:
        nonce = w3.eth.get_transaction_count(my_address)

        transaction = contract.functions.addModel(
            model_name, raw_key_bytes
        ).build_transaction(
            {
                "chainId": 11155111,  # Sepolia
                "gasPrice": w3.eth.gas_price,
                "from": my_address,
                "nonce": nonce,
            }
        )

        signed_txn = w3.eth.account.sign_transaction(
            transaction, private_key=private_key
        )
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

        print(f"Waiting for confirmation...")
        w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_hash.hex(), model_name

    except Exception as e:
        print(f"Debug Error: {e}")
        return False, None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to the .pem file")
    args = parser.parse_args()

    print(f"Processing file: {args.file}...")
    result, name = add_model_to_blockchain(args.file)

    if not result or result.startswith("Error"):
        print(f"Status: Failed - {result}")
    else:
        print(f"Status: Success")
        print(f"Model Name Registered: {name}")
        print(f"Transaction Hash: {result}")
