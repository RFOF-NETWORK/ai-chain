# api/register.py
# Registrierung-API: nutzt core.register (24-Wort-Phrase + Wallet-Adresse)

from core import register as core_register


def handle(vm, username: str, password: str, phrase: str = ""):
    """
    Registrierung eines neuen Users.
    phrase-Parameter wird ignoriert, da core.register selbst 24 Wörter generiert.
    Nutzt NICHT direkt vm.wallet.
    """
    result = core_register.register_user(username, password)

    if not result.get("success"):
        return {
            "status": "failed",
            "error": result.get("error", "REGISTER_FAILED")
        }

    # Optional: Blockchain-Zustand speichern, wenn vorhanden
    if hasattr(vm, "blockchain") and hasattr(vm.blockchain, "save_state"):
        vm.blockchain.save_state()

    return {
        "status": "ok",
        "username": result["username"],
        "address": result["wallet_address"],
        "mnemonic": result["mnemonic"]
    }

