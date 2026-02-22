# admin-rules.py
# RFOF-NETWORK Admin + User Security Pipeline
# ---------------------------------------------------------

import hashlib
import json
# Hinweis: bip39_library und rfof_gold_wordlist sind Platzhalter für deine Module
# import bip39_library 
# import rfof_gold_wordlist

# ---------------------------------------------------------
# LOAD USER DATABASE
# ---------------------------------------------------------
def load_users():
    try:
        with open("data/users.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

users = load_users()

# ---------------------------------------------------------
# HELPER: SAVE USERS
# ---------------------------------------------------------
def save_users():
    with open("data/users.json", "w") as f:
        json.dump(users, f, indent=4)

# ---------------------------------------------------------
# HELPER: HASH FUNCTION (PZQQET-Axiom)
# ---------------------------------------------------------
def make_hash(data):
    """
    PRAI-Standard: Double SHA256.
    Sichert die Unumkehrbarkeit der Admin- und User-IDs.
    """
    if isinstance(data, list):
        data = " ".join(data)
    
    # Der doppelte Hash-Vorgang nach PZQQET-Standard
    first_pass = hashlib.sha256(data.encode()).digest()
    return hashlib.sha256(first_pass).hexdigest()

# ---------------------------------------------------------
# ADMIN SOUVERÄNITÄT: 0,2-REGEL (ECCU LIMIT)
# ---------------------------------------------------------
def check_eccu_mint_limit(current_safe_value, requested_eccu_amount):
    """
    Prüft das PZQQET-Axiom: Admin kann 20 % des SAFE-Wertes als ECCU ausgeben.
    """
    max_mintable = current_safe_value * 0.2
    if requested_eccu_amount <= max_mintable:
        return True
    return False

# ---------------------------------------------------------
# ADMIN INITIALIZATION (ONE TIME)
# ---------------------------------------------------------
def init_admin(meta_phrase_48_words):

    # 1. SPLIT INTO BIP39 + RFOF PART (24 words each)
    bip39_part = meta_phrase_48_words[0:24]
    rfof_part  = meta_phrase_48_words[24:48]

    # 2. GENERATE ADMIN ADDRESS FROM BIP39 PART
    # Nutzt Double-SHA256 für die Adress-Generierung
    admin_address = "RFOF-ADMIN-" + make_hash(bip39_part)[:16]

    # 3. HASHES (PZQQET-Standard)
    bip39_hash = make_hash(bip39_part)
    rfof_hash  = make_hash(rfof_part)
    recovery_id = make_hash(" ".join(bip39_part) + "|" + " ".join(rfof_part))

    # 4. WRITE TO users.json
    users["RFOF-NETWORK"] = {
        "address": admin_address,
        "bip39_hash": bip39_hash,
        "rfof_hash": rfof_hash,
        "recovery_id": recovery_id,
        "role": "admin"
    }

    save_users()

# ---------------------------------------------------------
# CREATE NEW USER (AUTOMATIC)
# ---------------------------------------------------------
def create_user(username, bip39_phrase, rfof_phrase):

    # 1. GENERATE ADDRESS FROM BIP39
    address = "RFOF-USER-" + make_hash(bip39_phrase)[:16]

    # 2. HASHES (Double SHA256)
    bip39_hash = make_hash(bip39_phrase)
    rfof_hash  = make_hash(rfof_phrase)
    recovery_id = make_hash(" ".join(bip39_phrase) + "|" + " ".join(rfof_phrase))

    # 3. SAVE TO users.json
    users[username] = {
        "address": address,
        "bip39_hash": bip39_hash,
        "rfof_hash": rfof_hash,
        "recovery_id": recovery_id,
        "role": "user"
    }

    save_users()

    # 4. RETURN ONLY BIP39 PHRASE TO USER
    return {
        "status": "ok",
        "username": username,
        "address": address,
        "mnemonic": bip39_phrase
    }

# ---------------------------------------------------------
# VERIFY USER (ADMIN SUPPORT)
# ---------------------------------------------------------
def verify_user(username, user_bip39_phrase):

    if username not in users: 
        return False

    # 1. HASH USER INPUT (Double SHA256)
    input_hash = make_hash(user_bip39_phrase)

    # 2. COMPARE WITH STORED HASH
    return input_hash == users[username]["bip39_hash"]

# ---------------------------------------------------------
# RECOVERY PIPELINE (ADMIN ONLY)
# ---------------------------------------------------------
def recovery_pipeline(username, user_bip39_phrase):

    # 1. VERIFY USER
    if not verify_user(username, user_bip39_phrase):
        return "User verification failed"

    # 2. GET STORED RECOVERY ID
    recovery_id = users[username]["recovery_id"]

    # 3. RETURN RECOVERY TOKEN (ADMIN INTERNAL)
    return recovery_id
