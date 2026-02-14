# ---------------------------------------------------------
# admin-rules.py — PSEUDOCODE
# RFOF-NETWORK Admin + User Security Pipeline
# ---------------------------------------------------------

# IMPORTS (Pseudocode)
import bip39_library
import rfof_gold_wordlist
import hashing_library
import file_io_library


# ---------------------------------------------------------
# LOAD USER DATABASE
# ---------------------------------------------------------
users = load_json("data/users.json")


# ---------------------------------------------------------
# HELPER: SAVE USERS
# ---------------------------------------------------------
def save_users():
    write_json("data/users.json", users)


# ---------------------------------------------------------
# HELPER: HASH FUNCTION
# ---------------------------------------------------------
def make_hash(input_string):
    return hashing_library.sha256(input_string)


# ---------------------------------------------------------
# ADMIN INITIALIZATION (ONE TIME)
# ---------------------------------------------------------
def init_admin(meta_phrase_48_words):

    # 1. SPLIT INTO BIP39 + RFOF PART
    bip39_part = meta_phrase_48_words[0:24]
    rfof_part  = meta_phrase_48_words[24:48]

    # 2. VALIDATE BIP39 PART
    if not bip39_library.is_valid(bip39_part):
        raise Error("Invalid BIP39 admin phrase")

    # 3. GENERATE ADMIN ADDRESS FROM BIP39 PART
    admin_address = bip39_library.derive_address(bip39_part)

    # 4. HASHES
    bip39_hash = make_hash(join(bip39_part))
    rfof_hash  = make_hash(join(rfof_part))
    recovery_id = make_hash(join(bip39_part) + "|" + join(rfof_part))

    # 5. WRITE TO users.json
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
def create_user(username):

    # 1. GENERATE BIP39 PHRASE (VISIBLE TO USER)
    bip39_phrase = bip39_library.generate_24_words()

    # 2. GENERATE RFOF-GOLD PHRASE (INVISIBLE)
    rfof_phrase = rfof_gold_wordlist.generate_24_words()

    # 3. ADDRESS FROM BIP39
    address = bip39_library.derive_address(bip39_phrase)

    # 4. HASHES
    bip39_hash = make_hash(join(bip39_phrase))
    rfof_hash  = make_hash(join(rfof_phrase))
    recovery_id = make_hash(join(bip39_phrase) + "|" + join(rfof_phrase))

    # 5. SAVE TO users.json
    users[username] = {
        "address": address,
        "bip39_hash": bip39_hash,
        "rfof_hash": rfof_hash,
        "recovery_id": recovery_id,
        "role": "user"
    }

    save_users()

    # 6. RETURN ONLY BIP39 PHRASE TO USER
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

    # 1. HASH USER INPUT
    input_hash = make_hash(join(user_bip39_phrase))

    # 2. COMPARE WITH STORED HASH
    if input_hash == users[username]["bip39_hash"]:
        return True
    else:
        return False


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
