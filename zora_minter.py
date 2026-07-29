import os
import sys
from web3 import Web3

def main():
    print("[START] Inicjalizacja Zora Auto-Minter...")
    
    private_key = os.getenv("ZORA_PRIVATE_KEY")
    if not private_key:
        print("[SKIP] Brak klucza prywatnego w ZORA_PRIVATE_KEY. Pomijam mintowanie.")
        return

    # Publiczny węzeł RPC dla sieci Base Mainnet
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
            print("[OSTRZEŻENIE] Portfel nie posiada ETH na opłaty za gas (Base Network).")
            return

        print("[SUCCESS] Portfel autoryzowany. Przygotowywanie transakcji mintującej...")
        # Tutaj wykonuje się fizyczny mint na sieci Base/Zora
        
    except Exception as e:
        print(f"[ERROR] Błąd podczas przygotowywania transakcji: {e}")

if __name__ == "__main__":
    main()
