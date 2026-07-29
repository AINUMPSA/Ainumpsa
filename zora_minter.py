import json
import os
import time
from web3 import Web3

# ADRES TWOJEGO KONTRAKTU NA BASE
CONTRACT_ADDRESS = Web3.to_checksum_address(
    "0x84345EfC1a0aaEBCCfd7283eD3F4052f752d3A4b"
)


def main():
    print("\n[START] Inicjalizacja Zora Auto-Minter (Base Mainnet)...")

    # Pobieranie klucza z zmiennej środowiskowej
    private_key = os.environ.get("ZORA_PRIVATE_KEY")
    if not private_key or private_key == "YOUR_PRIVATE_KEY_HERE":
        print("[SKIP] Brak klucza prywatnego w ZORA_PRIVATE_KEY. Pomijam.")
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
        balance_eth = w3.from_wei(balance, "ether")
        print(f"[INFO] Stan konta: {balance_eth:.6f} ETH")

        if balance == 0:
            print("[OSTRZEŻENIE] Portfel nie posiada ETH na opłaty za gas.")
            return

        # Prawidłowe ABI dla kontraktu Zora ERC-1155
        zora_abi = [
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "minter",
                        "type": "address",
                    },
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "uint256", "name": "quantity", "type": "uint256"},
                    {"internalType": "bytes", "name": "minterArguments", "type": "bytes"},
                ],
                "name": "mint",
                "outputs": [],
                "stateMutability": "payable",
                "type": "function",
            }
        ]

        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=zora_abi)

        token_id = 1  # ID tokena do zmintowania
        quantity = 1  # Liczba sztuk
        minter_args = Web3.to_bytes(
            hexstr=f"0x000000000000000000000000{account.address[2:].lower()}"
        )

        # Standardowa opłata protokołu Zora
        mint_fee = w3.to_wei(0.000777, "ether")

        tx_data = contract.functions.mint(
            account.address, token_id, quantity, minter_args
        )

        # Szacowanie gazu
        estimated_gas = tx_data.estimate_gas(
            {"from": account.address, "value": mint_fee}
        )

        # Budowanie transakcji z identyfikatorem Base (8453)
        tx = tx_data.build_transaction({
            "from": account.address,
            "value": mint_fee,
            "nonce": w3.eth.get_transaction_count(account.address),
            "gas": int(estimated_gas * 1.2),
            "maxFeePerGas": w3.eth.gas_price,
            "maxPriorityFeePerGas": w3.to_wei(0.001, "gwei"),
            "chainId": 8453,
        })

        # Podpisanie i wysłanie
        signed_tx = account.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"[SUCCESS] Transakcja wysłana! Hash: {tx_hash.hex()}")

        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            print("[ZORA RESULT] NFT MINTED SUCCESSFULLY! 🎉")
        else:
            print("[ERROR] Transakcja odrzucona przez EVM.")

    except Exception as e:
        print(f"[ERROR] Błąd podczas wykonywania: {e}")


if __name__ == "__main__":
    main()
