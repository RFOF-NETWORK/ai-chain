# wallet/wallet_system.py

import hashlib


class WalletSystem:
    def __init__(self):
        self.users: dict[str, dict] = {}

    def register(self, username: str, password: str, phrase: str) -> str:
        address = hashlib.sha256(f"{username}{phrase}".encode()).hexdigest()
        self.users[username] = {
            "password": password,
            "phrase": phrase,
            "address": address
        }
        return address

    def login(self, username: str, password: str) -> str | None:
        user = self.users.get(username)
        if user and user["password"] == password:
            return user["address"]
        return None

    def offline_login(self, phrase: str) -> str | None:
        for user in self.users.values():
            if user["phrase"] == phrase:
                return user["address"]
        return None

