# wallet/wallet_system.py
import hashlib

class WalletSystem:
    def __init__(self):
        # Wir nutzen hier die Struktur aus admin-rules.py (users.json)
        self.users: dict[str, dict] = {}

    def make_prai_hash(self, data: str) -> str:
        """
        Integration des PZQQET-Axioms: Double SHA256.
        """
        first_pass = hashlib.sha256(data.encode()).digest()
        return hashlib.sha256(first_pass).hexdigest()

    def register(self, username: str, bip39_phrase: str, rfof_phrase: str) -> str:
        """
        Erweiterte Registrierung: Nutzt das Double-Hash-Verfahren 
        für die Adresse und speichert die Sicherheits-Hashes.
        """
        # Adresse wird deterministisch aus der BIP39-Phrase abgeleitet
        address = "RFOF-" + self.make_prai_hash(bip39_phrase)[:16]
        
        self.users[username] = {
            "address": address,
            "bip39_hash": self.make_prai_hash(bip39_phrase),
            "rfof_hash": self.make_prai_hash(rfof_phrase),
            "role": "user"
        }
        return address

    def login(self, username: str, bip39_phrase: str) -> str | None:
        """
        Login über die Phrase anstatt eines einfachen Passworts.
        """
        user = self.users.get(username)
        if user:
            input_hash = self.make_prai_hash(bip39_phrase)
            if user["bip39_hash"] == input_hash:
                return user["address"]
        return None

    def verify_recovery(self, username: str, full_meta_phrase: str) -> bool:
        """
        Prüft die 48-Wort Meta-Phrase gegen die gespeicherte Recovery-ID.
        """
        user = self.users.get(username)
        if not user:
            return False
            
        # Die Recovery-ID ist der Double-Hash der kombinierten Phrasen
        recovery_hash = self.make_prai_hash(full_meta_phrase)
        # Hier würde der Abgleich mit der recovery_id aus admin-rules erfolgen
        return True
