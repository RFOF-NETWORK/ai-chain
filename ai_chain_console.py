pimport hashlib
import time
import requests 


class AIChain:
    def __init__(self):

        # -------------------------------------------------
        # IDENTITÄT / ROOT
        # -------------------------------------------------
        # AI-CHAIN ROOT-ADRESSE (KEIN BTC/TON, INTERN, ADMIN-WALLET)
        self.admin_address = "1JGSqDHRoEfwLaB4wh9Up9j7NgckpyYYjZ"

        # 24-WORT ADMIN-PHRASE HASH (IDENTITÄTS-HASH)
        # = AI-CHAIN-WALLET-ADRESSE VON SATORIA
        self.genesis_hash = "d18e84a3edbf211e65fe60a715c5bfbe264f8ed635b96058cfbf69e44b56d541"

        # 48-WORT ADMIN-AP-PHRASE HASH (VALIDATION-HASH)
        # = AI-CHAIN-WALLET-ADRESSE VON SATORAMY
        self.genesis_validation_ap_hash = "5b3e57a9f4de5a155f5d7d33584467942b456d6e4b02f0139b47b0291f7e626b"

        self.founder_name = "Pinguin"
        self.org_legal_name = "Pinguin GbR"
        self.org_network_name = "RFOF-NETWORK"
        self.admin_login_name = "RFOF-NETWORK"

        # Externe, feste Admin-Auszahlungsanker (ECHTE BTC/TON)
        self.external_btc_address = "bc1qh7ucw0kmz0m3m808zhvxed46ma80f4yc92ph7d"
        self.external_ton_address = "UQDk-1Gqc4YIC22LTAAZLxomhkyp-V52B0yaeHgmk3t9Lli6"

        # -------------------------------------------------
        # LOGIN / PHRASES
        # -------------------------------------------------
        # username -> sha256(phrase)
        self.user_phrase_hashes = {}

        # -------------------------------------------------
        # CHAIN STATE
        # -------------------------------------------------
        self.chain = []
        self.difficulty = 5  # deterministisch, fix

        self.safe_value = 0.0
        self.trip = 0
        self.roundtrip = 0

        # -------------------------------------------------
        # TOKEN & PREISE
        # -------------------------------------------------
        self.ai_price = 1.25
        self.coin_price = 1.25
        self.lp_price = 2.50
        self.eccu_price = 2.50

        self.interaction_factor = 0.004  # 0,4 %

        # -------------------------------------------------
        # BALANCES & USER-PROFILE
        # -------------------------------------------------
        self.balances = {
            "system": {"AI": 0.0, "COIN": 0.0, "AIC-LP": 0.0, "ECCU": 0.0},
        }
        # username -> {"btc": str|None, "ton": str|None, "identity_hash": str|None, "ai_wallet": str|None}
        self.user_profiles = {}

        # -------------------------------------------------
        # ECCU / OWNER / FOND / SYSTEM
        # -------------------------------------------------
        self.owner = 0.0
        self.fond = 0.0
        self.system = 0.0

        self.layers = {
            "GlobalChain": 0.0,
            "ContinentalChain": 0.0,
            "CountryChain": 0.0,
            "FederalChain": 0.0,
            "CityChain": 0.0,
            "CommunityChain": 0.0,
        }

        # -------------------------------------------------
        # GENESIS
        # -------------------------------------------------
        self.create_genesis_block()
        self.setup_genesis_accounts()

    # ---------------------------------------------------------
    # HELFER
    # ---------------------------------------------------------

    def ensure_user(self, user):
        if user not in self.balances:
            self.balances[user] = {"AI": 0.0, "COIN": 0.0, "AIC-LP": 0.0, "ECCU": 0.0}
        if user not in self.user_profiles:
            self.user_profiles[user] = {
                "btc": None,
                "ton": None,
                "identity_hash": None,
                "ai_wallet": None,
            }

    # ---------------------------------------------------------
    # GENESIS BLOCK
    # ---------------------------------------------------------

    def create_genesis_block(self):
        block = {
            "index": 0,
            "timestamp": time.time(),
            "previous_hash": "0" * 64,
            "admin_address": self.admin_address,
            "genesis_hash": self.genesis_hash,
            "validation_hash": self.genesis_validation_ap_hash,
            "nonce": 0,
            "data": "GENESIS_BLOCK",
        }
        block["hash"] = self.hash_block(block)
        self.chain.append(block)
        print("[GENESIS BLOCK ERZEUGT]")

    # ---------------------------------------------------------
    # GENESIS-ACCOUNTS
    # ---------------------------------------------------------

    def setup_genesis_accounts(self):
        # alle drei teilen dieselbe 24-Wort-Phrase → deren Hash = genesis_hash
        shared_phrase_hash = self.genesis_hash

        # 1) Admin: RFOF-NETWORK
        self.ensure_user(self.admin_login_name)
        self.user_phrase_hashes[self.admin_login_name] = shared_phrase_hash
        self.user_profiles[self.admin_login_name]["btc"] = self.external_btc_address
        self.user_profiles[self.admin_login_name]["ton"] = self.external_ton_address
        # Admin AI-Chain-Wallet = admin_address
        self.user_profiles[self.admin_login_name]["ai_wallet"] = self.admin_address
        self.user_profiles[self.admin_login_name]["identity_hash"] = "ADMIN"

        # 2) Satoramy: Genesis-Kind mit Validation-Hash als AI-Chain-Wallet
        self.ensure_user("Satoramy")
        self.user_phrase_hashes["Satoramy"] = shared_phrase_hash
        self.user_profiles["Satoramy"]["identity_hash"] = self.genesis_validation_ap_hash
        self.user_profiles["Satoramy"]["ai_wallet"] = self.genesis_validation_ap_hash

        # 3) Satoria: Genesis-Kind mit Genesis-Hash als AI-Chain-Wallet
        self.ensure_user("Satoria")
        self.user_phrase_hashes["Satoria"] = shared_phrase_hash
        self.user_profiles["Satoria"]["identity_hash"] = self.genesis_hash
        self.user_profiles["Satoria"]["ai_wallet"] = self.genesis_hash

    # ---------------------------------------------------------
    # HASHING
    # ---------------------------------------------------------

    def hash_block(self, block):
        block_string = (
            str(block["index"])
            + str(block["timestamp"])
            + block["previous_hash"]
            + block["data"]
            + str(block["nonce"])
        )
        return hashlib.sha256(block_string.encode()).hexdigest()

    # ---------------------------------------------------------
    # TRIP & ROUNDTRIP
    # ---------------------------------------------------------

    def register_trip(self):
        self.trip += 1
        self.ai_price *= 1.002
        self.coin_price *= 1.002
        self.lp_price *= 1.004

        if self.trip % 10 == 0:
            self.roundtrip += 1
            self.update_roundtrip_prices()
            self.apply_safe_growth()
            self.apply_owner_fond_system()
            self.apply_eccu_distribution()

    def update_roundtrip_prices(self):
        self.ai_price = 1.25 * ((1 + self.interaction_factor) ** self.roundtrip)
        self.coin_price = self.ai_price
        self.lp_price = 2.50 * ((1 + self.interaction_factor * 2) ** self.roundtrip)

    # ---------------------------------------------------------
    # SAFE
    # ---------------------------------------------------------

    def apply_safe_growth(self):
        self.safe_value += 0.00315 * self.roundtrip
        print("[SAFE] SAFE =", self.safe_value)

    def add_safe_value(self, amount):
        # Energie-Zufluss (z.B. Fees, externe Energie), kein fester Genesis-Mint
        self.safe_value += amount
        print("[SAFE ERHÖHT] SAFE =", self.safe_value)

    # ---------------------------------------------------------
    # OWNER / FOND / SYSTEM
    # ---------------------------------------------------------

    def apply_owner_fond_system(self):
        A = self.safe_value
        self.owner = A * 0.00294
        self.fond = A * 0.00070
        self.system = A * 0.00021

        print("[OWNER/FOND/SYSTEM]")
        print("OWNER:", self.owner)
        print("FOND:", self.fond)
        print("SYSTEM:", self.system)

    # ---------------------------------------------------------
    # ECCU
    # ---------------------------------------------------------

    def apply_eccu_distribution(self):
        eccu_founder = self.safe_value * 0.02
        eccu_dist = self.safe_value * 0.18
        eccu_layer = eccu_dist / 6

        for k in self.layers:
            self.layers[k] = eccu_layer

        print("[ECCU VERTEILUNG]")
        print("Founder Reserve:", eccu_founder)

    # ---------------------------------------------------------
    # FEE SPLIT 45 / 42 / 10 / 3
    # ---------------------------------------------------------

    def apply_fee_split(self, fee_amount):
        self.system += fee_amount * 0.45
        self.owner += fee_amount * 0.42
        self.fond += fee_amount * 0.10
        self.safe_value += fee_amount * 0.03

    # ---------------------------------------------------------
    # TOKEN PREISE
    # ---------------------------------------------------------

    def get_price(self, token):
        if token == "AI":
            return self.ai_price
        if token == "COIN":
            return self.coin_price
        if token == "AIC-LP":
            return self.lp_price
        if token == "ECCU":
            return self.eccu_price
        raise ValueError("Unbekannter Token")

    # ---------------------------------------------------------
    # USER MINING
    # ---------------------------------------------------------

    def mine_user_block(self, data):
        print("[USER MINING]")
        previous_hash = self.chain[-1]["hash"]
        nonce = 0

        while True:
            block = {
                "index": len(self.chain),
                "timestamp": time.time(),
                "previous_hash": previous_hash,
                "data": data,
                "nonce": nonce,
            }
            block_hash = self.hash_block(block)

            if block_hash.startswith("0" * self.difficulty):
                block["hash"] = block_hash
                self.chain.append(block)
                print("[BLOCK GEFUNDEN]")
                self.register_trip()
                return

            nonce += 1

    # ---------------------------------------------------------
    # ADMIN MINT (OPTIONAL, KEIN GENESIS-MINT)
    # ---------------------------------------------------------

    def admin_mint(self, amount):
        print("[ADMIN MINT]")
        block = {
            "index": len(self.chain),
            "timestamp": time.time(),
            "previous_hash": self.chain[-1]["hash"],
            "data": f"ADMIN_MINT {amount}",
            "nonce": 0,
        }
        block["hash"] = self.hash_block(block)
        self.chain.append(block)
        self.register_trip()

    # ---------------------------------------------------------
    # SWAP
    # ---------------------------------------------------------

    def swap_tokens(self, user, token_from, token_to, amount_from):
        self.ensure_user(user)
        price_from = self.get_price(token_from)
        price_to = self.get_price(token_to)

        value = amount_from * price_from
        amount_to = value / price_to

        fee = value * 0.01
        self.apply_fee_split(fee)

        self.balances[user][token_from] -= amount_from
        self.balances[user][token_to] += amount_to

        self.register_trip()

        print("[SWAP]", user, amount_from, token_from, "→", amount_to, token_to)

    # ---------------------------------------------------------
    # SENDEN
    # ---------------------------------------------------------

    def send_tokens(self, sender, receiver, token, amount):
        self.ensure_user(sender)
        self.ensure_user(receiver)

        self.balances[sender][token] -= amount
        self.balances[receiver][token] += amount

        print("[SEND]", sender, "→", receiver, amount, token)

    # ---------------------------------------------------------
    # BTC/TON ADRESSEN
    # ---------------------------------------------------------

    def set_btc_address(self, user):
        self.ensure_user(user)
        addr = input("BTC-Adresse: ").strip()
        self.user_profiles[user]["btc"] = addr
        print("[BTC] Gesetzt für", user, "→", addr)

    def set_ton_address(self, user):
        self.ensure_user(user)
        addr = input("TON-Adresse: ").strip()
        self.user_profiles[user]["ton"] = addr
        print("[TON] Gesetzt für", user, "→", addr)

    # ---------------------------------------------------------
    # AUSZAHLUNG: USER (AI/COIN → BTC/TON)
    # ---------------------------------------------------------

    def user_payout_token_btc(self):
        user = self.current_user
        self.ensure_user(user)
        token = input("Token (AI/COIN): ").strip()
        amount = float(input("Menge: "))
        btc = self.user_profiles[user]["btc"]
        if not btc:
            print("Keine BTC-Adresse für", user)
            return
        self.balances[user][token] -= amount
        print("[USER PAYOUT]", user, token, amount, "→", btc)

    def user_payout_token_ton(self):
        user = self.current_user
        self.ensure_user(user)
        token = input("Token (AI/COIN): ").strip()
        amount = float(input("Menge: "))
        ton = self.user_profiles[user]["ton"]
        if not ton:
            print("Keine TON-Adresse für", user)
            return
        self.balances[user][token] -= amount
        print("[USER PAYOUT]", user, token, amount, "→", ton)

    # ---------------------------------------------------------
    # AUSZAHLUNG: ADMIN (ECCU → BTC/TON)
    # ---------------------------------------------------------

    def admin_payout_eccu_btc(self):
        user = input("User: ").strip()
        self.ensure_user(user)
        amount = float(input("ECCU-Menge: "))
        self.balances[user]["ECCU"] -= amount
        print("[ADMIN PAYOUT ECCU→BTC]", user, amount, "→", self.external_btc_address)

    def admin_payout_eccu_ton(self):
        user = input("User: ").strip()
        self.ensure_user(user)
        amount = float(input("ECCU-Menge: "))
        self.balances[user]["ECCU"] -= amount
        print("[ADMIN PAYOUT ECCU→TON]", user, amount, "→", self.external_ton_address)

    # ---------------------------------------------------------
    # LOGIN MIT PHRASE (24 für alle, 48 zusätzlich nur für Admin)
    # ---------------------------------------------------------

    def login(self):
        username = input("Benutzername: ").strip()
        phrase = input("Phrase (alle Wörter in einer Zeile): ").strip()

        phrase_hash = hashlib.sha256(phrase.encode()).hexdigest()

        # ADMIN: RFOF-NETWORK
        if username == self.admin_login_name:
            # 24-Wort-Login (shared_phrase_hash == genesis_hash)
            if phrase_hash == self.genesis_hash:
                self.ensure_user(username)
                self.current_user = username
                print("[ADMIN LOGIN OK mit 24-Wort-Phrase]", username)
                return
            # 48-Wort-Login (AP-Validation)
            if phrase_hash == self.genesis_validation_ap_hash:
                self.ensure_user(username)
                self.current_user = username
                print("[ADMIN LOGIN OK mit 48-Wort-AP-Phrase]", username)
                return
            print("Falsche Admin-Phrase.")
            return

        # NORMALE USER (inkl. Satoramy, Satoria)
        self.ensure_user(username)

        # falls noch nicht registriert (neue User)
        if username not in self.user_phrase_hashes:
            self.user_phrase_hashes[username] = phrase_hash
            self.current_user = username
            print("[USER REGISTRIERT & EINGELOGGT]", username)
            return

        # bestehende User (inkl. Genesis-Kinder)
        if self.user_phrase_hashes[username] == phrase_hash:
            self.current_user = username
            print("[LOGIN OK]", username)
        else:
            print("Falsche Phrase für diesen Benutzer.")

    # ---------------------------------------------------------
    # WALLET
    # ---------------------------------------------------------

    def show_wallet(self):
        self.ensure_user(self.current_user)
        print("Wallet:", self.balances[self.current_user])
        print("Profile:", self.user_profiles[self.current_user])

    # ---------------------------------------------------------
    # KONSOLE
    # ---------------------------------------------------------

    def start_console(self):
        self.current_user = None

        while True:
            print("\n--- AI-CHAIN KONSOLE (ECCU-CODESPRACHE) ---")
            print("1. Login (mit Phrase)")
            print("2. Wallet")
            print("3. Swap")
            print("4. Senden")
            print("5. BTC-Adresse setzen")
            print("6. TON-Adresse setzen")
            print("7. Auszahlung → BTC")
            print("8. Auszahlung → TON")
            print("A1. Admin ECCU → BTC")
            print("A2. Admin ECCU → TON")
            print("M. Mining")
            print("0. Exit")

            c = input("Auswahl: ").strip()

            if c == "1":
                self.login()
            elif c == "2":
                if self.current_user:
                    self.show_wallet()
                else:
                    print("Bitte zuerst einloggen.")
            elif c == "3":
                if not self.current_user:
                    print("Bitte zuerst einloggen.")
                    continue
                t1 = input("Von: ")
                t2 = input("Zu: ")
                a = float(input("Menge: "))
                self.swap_tokens(self.current_user, t1, t2, a)
            elif c == "4":
                if not self.current_user:
                    print("Bitte zuerst einloggen.")
                    continue
                r = input("Empfänger: ")
                t = input("Token: ")
                a = float(input("Menge: "))
                self.send_tokens(self.current_user, r, t, a)
            elif c == "5":
                if not self.current_user:
                    print("Bitte zuerst einloggen.")
                    continue
                self.set_btc_address(self.current_user)
            elif c == "6":
                if not self.current_user:
                    print("Bitte zuerst einloggen.")
                    continue
                self.set_ton_address(self.current_user)
            elif c == "7":
                if not self.current_user:
                    print("Bitte zuerst einloggen.")
                    continue
                self.user_payout_token_btc()
            elif c == "8":
                if not self.current_user:
                    print("Bitte zuerst einloggen.")
                    continue
                self.user_payout_token_ton()
            elif c.upper() == "A1":
                if self.current_user == self.admin_login_name:
                    self.admin_payout_eccu_btc()
                else:
                    print("Nur Admin!")
            elif c.upper() == "A2":
                if self.current_user == self.admin_login_name:
                    self.admin_payout_eccu_ton()
                else:
                    print("Nur Admin!")
            elif c.upper() == "M":
                d = input("Mining-Daten: ")
                self.mine_user_block(d)
            elif c == "0":
                break


# ---------------------------------------------------------
# START
# ---------------------------------------------------------

if __name__ == "__main__":
    chain = AIChain()
    chain.start_console()
# -------------------------------------------------
        # EXTERNE NODE-ANBINDUNG (BTC CORE / TON CORE)
        # -------------------------------------------------
        # BTC Core JSON-RPC (lokaler oder externer Node)
        self.btc_rpc_url = "http://127.0.0.1:8332"
        self.btc_rpc_user = "user"
        self.btc_rpc_password = "pass"

        # TON "Core" / HTTP-API / Toncenter / eigene Node
        self.ton_api_url = "https://toncenter.com/api/v2/jsonRPC"
        self.ton_api_key = "DEIN_TON_API_KEY"  # falls nötig, sonst None

        # interne Mapping-Tabellen für Einzahlungen
        # externe Adresse → interner User
        self.btc_deposit_map = {}  # z.B. {"bc1xyz...": "Satoramy"}
        self.ton_deposit_map = {}  # z.B. {"UQxyz...": "Satoramy"} 
# -------------------------------------------------
    # BTC CORE RPC-CLIENT
    # -------------------------------------------------

    def btc_rpc_call(self, method, params=None):
        if params is None:
            params = []
        payload = {
            "jsonrpc": "1.0",
            "id": "aichain",
            "method": method,
            "params": params,
        }
        r = requests.post(
            self.btc_rpc_url,
            json=payload,
            auth=(self.btc_rpc_user, self.btc_rpc_password),
            timeout=10,
        )
        r.raise_for_status()
        data = r.json()
        if data.get("error"):
            raise RuntimeError(f"BTC RPC Error: {data['error']}")
        return data["result"]
# -------------------------------------------------
    # TON API-CLIENT
    # -------------------------------------------------

    def ton_api_call(self, method, params=None):
        if params is None:
            params = {}
        payload = {
            "jsonrpc": "2.0",
            "id": "aichain",
            "method": method,
            "params": params,
        }
        headers = {}
        if self.ton_api_key:
            headers["X-API-Key"] = self.ton_api_key

        r = requests.post(
            self.ton_api_url,
            json=payload,
            headers=headers,
            timeout=10,
        )
        r.raise_for_status()
        data = r.json()
        if "error" in data and data["error"]:
            raise RuntimeError(f"TON API Error: {data['error']}")
        return data["result"]

# -------------------------------------------------
    # EXTERNE EINZAHLUNG: BTC → INTERNE TOKENS
    # -------------------------------------------------

    def register_btc_deposit_address(self, user, btc_address):
        """
        Verknüpft eine BTC-Adresse mit einem internen User für automatische Gutschriften.
        """
        self.ensure_user(user)
        self.btc_deposit_map[btc_address] = user
        print("[BTC DEPOSIT MAP] ", btc_address, "→", user)

    def scan_btc_deposits(self, min_conf=1, token="AI"):
        """
        Liest BTC-Core-Transaktionen und schreibt interne Gutschriften gut.
        Vereinfachte Variante: listtransactions + Mapping.
        """
        print("[BTC DEPOSIT SCAN]")
        txs = self.btc_rpc_call("listtransactions", ["*", 100])
        for tx in txs:
            if not tx.get("address"):
                continue
            addr = tx["address"]
            amount = tx.get("amount", 0.0)
            confirmations = tx.get("confirmations", 0)
            category = tx.get("category")

            if category != "receive":
                continue
            if confirmations < min_conf:
                continue
            if addr not in self.btc_deposit_map:
                continue

            user = self.btc_deposit_map[addr]
            self.ensure_user(user)

            # BTC-Wert → interne Token (z.B. 1 BTC = X AI)
            # Hier: einfacher 1:1-Wert in AI-Preis-Einheiten
            value_in_fiat = amount  # Platzhalter: 1 BTC = 1 "Wert"
            token_price = self.get_price(token)
            token_amount = value_in_fiat / token_price

            self.balances[user][token] += token_amount
            print("[BTC DEPOSIT CREDIT]", user, token_amount, token, "für", amount, "BTC an", addr)

# -------------------------------------------------
    # EXTERNE EINZAHLUNG: TON → INTERNE TOKENS
    # -------------------------------------------------

    def register_ton_deposit_address(self, user, ton_address):
        self.ensure_user(user)
        self.ton_deposit_map[ton_address] = user
        print("[TON DEPOSIT MAP] ", ton_address, "→", user)

    def scan_ton_deposits(self, token="AI"):
        """
        Beispielhaft: du musst hier die konkrete TON-API anpassen.
        Idee: getTransactions(address) → Mapping → Gutschrift.
        """
        print("[TON DEPOSIT SCAN]")
        for addr, user in self.ton_deposit_map.items():
            # Pseudocode – API hängt von deinem Provider ab
            try:
                result = self.ton_api_call("getTransactions", {"address": addr})
            except Exception as e:
                print("[TON API ERROR]", e)
                continue

            # result-Struktur hängt von API ab – hier nur Platzhalter
            txs = result.get("transactions", [])
            for tx in txs:
                amount = tx.get("amount", 0.0)
                incoming = tx.get("incoming", True)
                if not incoming:
                    continue

                self.ensure_user(user)
                value_in_fiat = amount  # Platzhalter
                token_price = self.get_price(token)
                token_amount = value_in_fiat / token_price

                self.balances[user][token] += token_amount
                print("[TON DEPOSIT CREDIT]", user, token_amount, token, "für", amount, "TON an", addr)


# -------------------------------------------------
    # EXTERNE AUSZAHLUNG: INTERNE TOKENS → BTC CORE
    # -------------------------------------------------

    def user_payout_token_btc_onchain(self):
        user = self.current_user
        self.ensure_user(user)
        token = input("Token (AI/COIN): ").strip()
        amount = float(input("Menge: "))

        btc = self.user_profiles[user]["btc"]
        if not btc:
            print("Keine BTC-Adresse für", user)
            return

        # interner Abzug
        self.balances[user][token] -= amount

        # Wert in BTC (Platzhalter: 1 Token = 1 BTC-Einheit / Preis)
        value = amount * self.get_price(token)
        btc_amount = value  # hier musst du deine eigene Logik definieren

        # BTC-Core-Transaktion bauen
        try:
            txid = self.btc_rpc_call("sendtoaddress", [btc, btc_amount])
            print("[USER PAYOUT BTC ONCHAIN]", user, token, amount, "→", btc_amount, "BTC an", btc, "TXID:", txid)
        except Exception as e:
            print("[BTC PAYOUT ERROR]", e)

# -------------------------------------------------
    # EXTERNE AUSZAHLUNG: INTERNE TOKENS → TON
    # -------------------------------------------------

    def user_payout_token_ton_onchain(self):
        user = self.current_user
        self.ensure_user(user)
        token = input("Token (AI/COIN): ").strip()
        amount = float(input("Menge: "))

        ton = self.user_profiles[user]["ton"]
        if not ton:
            print("Keine TON-Adresse für", user)
            return

        self.balances[user][token] -= amount

        value = amount * self.get_price(token)
        ton_amount = value  # Platzhalter

        # TON-Transfer – API hängt von deinem Provider ab
        try:
            result = self.ton_api_call("sendTransaction", {
                "to": ton,
                "amount": ton_amount,
            })
            print("[USER PAYOUT TON ONCHAIN]", user, token, amount, "→", ton_amount, "TON an", ton, "RESULT:", result)
        except Exception as e:
            print("[TON PAYOUT ERROR]", e)

# -------------------------------------------------
    # STAKING-MODUL
    # -------------------------------------------------

    def stake_ai(self, user, amount):
        """
        Einfaches Staking: AI wird gelockt, SAFE wächst, später Claim möglich.
        """
        self.ensure_user(user)
        if self.balances[user]["AI"] < amount:
            print("Zu wenig AI zum Staken.")
            return

        if not hasattr(self, "staking_positions"):
            self.staking_positions = {}

        self.balances[user]["AI"] -= amount
        pos = {
            "amount": amount,
            "start_roundtrip": self.roundtrip,
        }
        self.staking_positions.setdefault(user, []).append(pos)
        print("[STAKING] ", user, "staked", amount, "AI")

    def claim_staking_rewards(self, user):
        """
        Rewards = amount * (roundtrip_diff * Faktor)
        """
        self.ensure_user(user)
        if not hasattr(self, "staking_positions"):
            print("Keine Staking-Positionen.")
            return

        positions = self.staking_positions.get(user, [])
        if not positions:
            print("Keine Staking-Positionen für", user)
            return

        total_reward = 0.0
        new_positions = []
        for pos in positions:
            diff = self.roundtrip - pos["start_roundtrip"]
            if diff <= 0:
                new_positions.append(pos)
                continue
            reward = pos["amount"] * diff * 0.001  # Faktor frei definierbar
            total_reward += reward

        self.staking_positions[user] = new_positions
        self.balances[user]["AI"] += total_reward
        print("[STAKING REWARD]", user, total_reward, "AI")

# -------------------------------------------------
    # ANALYTICS / METRICS
    # -------------------------------------------------

    def show_chain_metrics(self):
        print("----- AI-CHAIN METRICS -----")
        print("Blöcke:", len(self.chain))
        print("SAFE:", self.safe_value)
        print("Trip:", self.trip)
        print("Roundtrip:", self.roundtrip)
        print("OWNER:", self.owner)
        print("FOND:", self.fond)
        print("SYSTEM:", self.system)
        print("Layer:", self.layers)
        print("User:", list(self.balances.keys()))

# -------------------------------------------------
# SYSTEM-HEALTH / SELF-DIAGNOSTICS
# -------------------------------------------------
def system_health(self):
        return {
            "chain_length": len(self.chain),
            "last_block_hash": self.chain[-1]["hash"] if self.chain else None,
            "roundtrip": self.roundtrip,
            "trip": self.trip,
            "safe": self.safe_value,
            "eccu_total": self.eccu_total if hasattr(self, "eccu_total") else None,
            "registered_users": list(self.balances.keys()),
            "btc_rpc_online": self._check_btc_rpc(),
            "ton_api_online": self._check_ton_api(),
            "staking_positions": {
                u: len(p) for u, p in self.staking_positions.items()
            } if hasattr(self, "staking_positions") else {},
        }

    def _check_btc_rpc(self):
        try:
            self.btc_rpc_call("getblockcount")
            return True
        except:
            return False

    def _check_ton_api(self):
        try:
            self.ton_api_call("getMasterchainInfo")
            return True
        except:
            return False

# -------------------------------------------------
# CONSENSUS / BLOCK-VALIDATION
# -------------------------------------------------
def validate_block(self, block):
        if "index" not in block or "timestamp" not in block or "data" not in block:
            return False
        if "prev_hash" not in block or "hash" not in block or "nonce" not in block:
            return False

        recalculated = self.hash_block({
            "index": block["index"],
            "timestamp": block["timestamp"],
            "data": block["data"],
            "prev_hash": block["prev_hash"],
            "nonce": block["nonce"],
        })

        if recalculated != block["hash"]:
            return False

        if not block["hash"].startswith("0" * self.difficulty):
            return False

        return True

    def validate_chain(self):
        if not self.chain:
            return False

        for i in range(1, len(self.chain)):
            prev = self.chain[i - 1]
            curr = self.chain[i]

            if curr["prev_hash"] != prev["hash"]:
                return False

            if not self.validate_block(curr):
                return False

        return True
# -------------------------------------------------
# SYSTEM-INTEGRATION / SELF-LINKING ENGINE
# -------------------------------------------------

    def integrate_system(self):
        return {
            "identity_root": hasattr(self, "owner") and hasattr(self, "fond") and hasattr(self, "system"),
            "login_ready": hasattr(self, "current_user"),
            "chain_ready": isinstance(self.chain, list) and len(self.chain) > 0,
            "hashing_ready": callable(getattr(self, "hash_block", None)),
            "mining_ready": callable(getattr(self, "mine_user_block", None)),
            "trip_roundtrip_ready": hasattr(self, "trip") and hasattr(self, "roundtrip"),
            "safe_ready": hasattr(self, "safe_value"),
            "eccu_ready": hasattr(self, "eccu_total") or hasattr(self, "eccu"),
            "swap_ready": callable(getattr(self, "swap_tokens", None)),
            "send_ready": callable(getattr(self, "send_token", None)),
            "btc_bridge_ready": hasattr(self, "btc_rpc_url") and callable(getattr(self, "btc_rpc_call", None)),
            "ton_bridge_ready": hasattr(self, "ton_api_url") and callable(getattr(self, "ton_api_call", None)),
            "deposit_ready": hasattr(self, "btc_deposit_map") and hasattr(self, "ton_deposit_map"),
            "payout_ready": callable(getattr(self, "user_payout_token_btc_onchain", None)) and callable(getattr(self, "user_payout_token_ton_onchain", None)),
            "staking_ready": hasattr(self, "staking_positions"),
            "analytics_ready": callable(getattr(self, "show_chain_metrics", None)),
            "health_ready": callable(getattr(self, "system_health", None)),
            "consensus_ready": callable(getattr(self, "validate_chain", None)),
            "full_system_ready": all([
                hasattr(self, "owner"),
                hasattr(self, "fond"),
                hasattr(self, "system"),
                hasattr(self, "chain"),
                hasattr(self, "difficulty"),
                hasattr(self, "trip"),
                hasattr(self, "roundtrip"),
                hasattr(self, "safe_value"),
                hasattr(self, "balances"),
                hasattr(self, "staking_positions"),
                callable(getattr(self, "hash_block", None)),
                callable(getattr(self, "validate_chain", None)),
                callable(getattr(self, "system_health", None)),
            ])
        }

    def print_system_integration(self):
        status = self.integrate_system()
        print("----- SYSTEM-INTEGRATION STATUS -----")
        for key, value in status.items():
            print(f"{key}: {value}")

