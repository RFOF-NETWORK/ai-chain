# core/hash-generator.py
# Double SHA-256 für Admin-Phrase (offline)

import hashlib
import sys

def double_sha256(data: str) -> str:
    b = data.encode("utf-8")
    return hashlib.sha256(hashlib.sha256(b).digest()).hexdigest()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python hash-generator.py \"word1 word2 ... word24\"")
        sys.exit(1)

    phrase = sys.argv[1]
    print(double_sha256(phrase))
