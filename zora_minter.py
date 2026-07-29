import os
import time
import json
from web3 import Web3

# TWOJ ADRES KONTRAKTU – wpisany tutaj
CONTRACT_ADDRESS = "0x84345EfC1a0aaEBCCfd7283eD3F4052f752d3A4b"

def main():
    print("\n[START] Inicjalizacja Zora Auto-Minter (REAL MINT)...")

    private_key = os.environ.get("ZORA_PRIVATE_KEY")
    if not private_key or private_key == "YOUR_PRIVATE_KEY_HERE":
        print("[SKIP] Brak klucza prywatnego. Pomijam mintowanie.")
        return

    rpc_url = "https://mainnet.base.org"
    w3 = Web3(Web3.HTTPProvider(rpc_url))

    if not w3.is_connected():
        print("[ERROR] Nie udało się połączyć z siecią Base Mainnet.")
        return

    try:
        account = w3.eth.account.from_key(private_key)
        print(f"[INFO] Połączono z portfelem: {account.address}")

        balance = w3.eth.get_balance(account.address)
        balance_eth = w3.from_wei(balance, 'ether')
        print(f"[INFO] Stan konta: {balance_eth:.6f} ETH")

        if balance == 0:
            print("[OSTRZEŻENIE] Portfel nie posiada ETH na opłaty za gas.")
            return

        # Wczytaj metadane (jeśli istnieją)
        token_uri = "ipfs://QmExample"  # <- TU WPISZ LINK DO METADANYCH
        if os.path.exists("metadata.json"):
            with open("metadata.json", "r") as f:
                metadata = json.load(f)
                token_uri = metadata.get("image", token_uri)
            print("[INFO] Wczytano metadane z metadata.json")

        # Minimalne ABI dla mintowania (ERC-721)
        abi = [
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "string", "name": "uri", "type": "string"}
                ],
                "name": "mint",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            }
        ]

        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

        # Budowanie transakcji
        tx = contract.functions.mint(account.address, token_uri).build_transaction({
            "from": account.address,
            "nonce": w3.eth.get_transaction_count(account.address),
            "gas": 200000,
            "gasPrice": w3.eth.gas_price,
        })

        # Podpisanie i wysłanie
        signed_tx = account.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"[SUCCESS] Transakcja wysłana! Hash: {tx_hash.hex()}")

        # Czekamy na potwierdzenie
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            print("[ZORA RESULT] NFT MINTED! 🎉")
        else:
            print("[ERROR] Transakcja nie powiodła się.")

    except Exception as e:
        print(f"[ERROR] Błąd: {e}")

if __name__ == "__main__":
    main()
