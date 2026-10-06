#!/usr/bin/env python3
"""
AINUMPSA – Zora Auto-Minter (v2.3 – Zintegrowany z Tensor T i nft_ready)
"""

import os
import json
import time
from pathlib import Path
from web3 import Web3

NFT_READY_DIR = Path("nft_ready")
CONTRACT_ADDRESS = Web3.to_checksum_address("0x84345EfC1a0aaEBCCfd7283eD3F4052f752d3A4b")

def get_latest_nft_payload():
    """Przeszukuje katalog nft_ready w poszukiwaniu najnowszych wyemitowanych tokenów"""
    if not NFT_READY_DIR.exists():
        return None
    
    files = sorted(
        [f for f in NFT_READY_DIR.iterdir() if f.is_file() and f.suffix == '.json'],
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )
    if not files:
        return None
    
    try:
        with open(files[0], "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[WARN] Nie można odczytać pliku payloadu NFT: {e}")
        return None

def main():
    print("\n[START] Inicjalizacja Zora Auto-Minter (Base Mainnet)...")

    # 1. Sprawdzanie uwierzytelnienia klucza w GitHub Secrets
    private_key = os.environ.get("ZORA_PRIVATE_KEY")
    if not private_key or private_key == "YOUR_PRIVATE_KEY_HERE":
        print("[SKIP] Brak klucza prywatnego w zmiennych środowiskowych ZORA_PRIVATE_KEY. Pomijam proces blockchain.")
        return

    # 2. Pobieranie dynamicznego sygnału z matrycy
    payload = get_latest_nft_payload()
    if not payload:
        print("[SKIP] Brak nowych wyemitowanych struktur w nft_ready/. Czekam na rezonans pola.")
        return
        
    print(f"[QUANTUM COUPLING] Wykryto plik gotowy do emisji: {payload.get('source', 'Nieznane źródło')}")

    rpc_url = "https://mainnet.base.org"
    w3 = Web3(Web3.HTTPProvider(rpc_url))

    if not w3.is_connected():
        print("[ERROR] Brak łączności z węzłem Base Mainnet.")
        return

    try:
        account = w3.eth.account.from_key(private_key)
        print(f"[INFO] Autoryzacja portfela powiodła się: {account.address}")

        balance = w3.eth.get_balance(account.address)
        balance_eth = w3.from_wei(balance, "ether")
        print(f"[INFO] Stan środków portfela: {balance_eth:.6f} ETH")

        if balance == 0:
            print("[OSTRZEŻENIE] Brak ETH w portfelu. Wymagane zasilenie konta na Base na pokrycie opłat.")
            return

        # Prawidłowe ABI dla kontraktu Zora ERC-1155
        zora_abi = [
            {
                "inputs": [
                    {"internalType": "address", "name": "minter", "type": "address"},
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

        # Dynamicznie pobieramy ID oraz ilość z wygenerowanego pliku JSON
        token_id = int(payload.get("token_id", 1))
        # Możesz ustawić pobieranie dynamicznej ilości, np: int(payload.get("quantity", 1))
        quantity = 1  
        
        minter_args = Web3.to_bytes(
            hexstr=f"0x000000000000000000000000{account.address[2:].lower()}"
        )

        # Standardowa stała opłata protokołu Zora mintFee
        mint_fee = w3.to_wei(0.000777, "ether") * quantity

        tx_data = contract.functions.mint(
            account.address, token_id, quantity, minter_args
        )

        # Dynamiczne szacowanie limitu gazu
        estimated_gas = tx_data.estimate_gas(
            {"from": account.address, "value": mint_fee}
        )

        # Dynamiczne pobieranie aktualnych stawek Base w celu uniknięcia utknięcia tx
        current_gas_price = w3.eth.gas_price
        max_priority_fee = w3.to_wei(0.1, "gwei") # Bezpieczny próg dla Base
        
        tx = tx_data.build_transaction({
            "from": account.address,
            "value": mint_fee,
            "nonce": w3.eth.get_transaction_count(account.address),
            "gas": int(estimated_gas * 1.25), # Zapas 25% bezpieczeństwa
            "maxFeePerGas": int(current_gas_price * 1.3), # Zapas ceny gazu
            "maxPriorityFeePerGas": max_priority_fee,
            "chainId": 8453,
        })

        # Podpis i transmisja na blockchain
        print(f"[TRANSMISSION] Wysyłam żądanie zapisu bloku na Base...")
        signed_tx = account.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"[SUCCESS] Transakcja wstrzyknięta do sieci! Hash: {tx_hash.hex()}")

        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        if receipt.status == 1:
            print(f"[ZORA RESULT] MATRYCA UWIERZYTELNIONA NA BASE ON-CHAIN! NFT TOKEN {token_id} MINTED 🎉")
        else:
            print("[ERROR] Transakcja została zrzucona (Reverted) przez EVM Base.")

    except Exception as e:
        print(f"[ERROR] Awaria potoku wykonawczego Zora: {e}")

if __name__ == "__main__":
    main()
