import sys
from mnemonic import Mnemonic
import bip32utils
import hashlib

def phrase_to_seed(phrase: str) -> bytes:
    mnemo = Mnemonic("english")
    return mnemo.to_seed(phrase)

def seed_to_wallet_address(seed: bytes) -> str:
    root_key = bip32utils.BIP32Key.fromEntropy(seed)

    # Ableitungspfad m/44'/0'/0'/0/0
    child_key = (
        root_key
        .ChildKey(44 + bip32utils.BIP32_HARDEN)
        .ChildKey(0 + bip32utils.BIP32_HARDEN)
        .ChildKey(0 + bip32utils.BIP32_HARDEN)
        .ChildKey(0)
        .ChildKey(0)
    )

    return child_key.Address()

def double_sha256(data: str) -> str:
    b = data.encode("utf-8")
    return hashlib.sha256(hashlib.sha256(b).digest()).hexdigest()

def main():
    if len(sys.argv) < 2:
        print("Bitte 48-Wort-Phrase als Argument übergeben.")
        sys.exit(1)

    phrase = sys.argv[1]
    seed = phrase_to_seed(phrase)
    wallet_address = seed_to_wallet_address(seed)
    identity_hash = double_sha256(wallet_address)

    print("Wallet-Adresse:", wallet_address)
    print("Identitäts-Hash (Double SHA-256):", identity_hash)

if __name__ == "__main__":
    main()
