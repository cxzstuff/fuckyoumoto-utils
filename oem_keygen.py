import sys
from hashlib import sha256

def oem_keygen(key: str) -> str:
    to_hash: str = key * 2
    print("To hash: ", to_hash)

    hash: str = sha256(to_hash.encode()).hexdigest()

    print("Hash: ", hash)
    print("Possible keys:\n%s\n%s" % (hash[:32], hash[32:]))
    print("Capitalized:\n%s\n%s" % (hash[:32].upper(), hash[32:].upper()))
    return hash


if __name__ == "__main__":
    if not len(sys.argv) == 2:
        print("Usage: python3 oem_keygen.py <key>")
        print("First run `fastboot oem get_key` to get the key")
        sys.exit(0)

    if not len(sys.argv[1]) == 32:
        print("Key must be 32 characters long.)
        sys.exit(1)

    oem_keygen(sys.argv[1])
