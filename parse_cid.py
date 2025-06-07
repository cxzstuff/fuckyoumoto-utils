import sys
from cryptography import x509, x509
from cryptography.x509.base import Certificate
from cryptography.hazmat.backends import default_backend
from typing import Dict, Optional

def parse_cid(cid_data: bytes) -> Dict[str, str]:
    if len(cid_data) < 0x70:
        raise ValueError("CID data length is too short. Recheck the file.")
    

    # CID v1 uses sha1 for the unlock code
    # CID v2 uses sha256 for the unlock code
    cid_db_version = cid_data[0x03]

    bootloader_uid = cid_data[0x08:0x18]
    # Imei first byte contains an A, because IMEI are 15 digits long, so
    # it is padded with an A to make it 16 bytes.
    imei = cid_data[0x30:0x38]
    serial_number = cid_data[0x3A:0x4E]
    phone_hash = cid_data[0x50:0x70]
    cid_value = cid_data[0x2D]

    return {
        "cid_db_version": str(cid_db_version),
        "cid_value": "0x{:02X}".format(cid_value),
        "bootloader_uid": bootloader_uid.hex(),
        "imei": imei.hex(),
        "serial_number": serial_number.hex(),
        "phone_hash": phone_hash.hex(),
    }


def parse_certificate(cert_data: bytes) -> Certificate:
    try:
        cert: Certificate = x509.load_der_x509_certificate(cert_data, default_backend())
    except ValueError as e:
        raise ValueError(f"Invalid certificate data: {e}")
    
    return cert

def get_unlock_data(cid_dict: Dict[str, str]) -> str:
    """
    Returns the unlock data if available in the CID dictionary.
    """
    return "#".join(
        [
            cid_dict.get("imei", ""),
            cid_dict.get("serial_number", ""),
            cid_dict.get("phone_hash", ""),
            cid_dict.get("bootloader_uid", ""),
        ]
    )

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python parse_cid.py <cid-file>")
        sys.exit(1)
    

    with open(sys.argv[1], 'rb') as f:
        cid_data = f.read()
    
    try:
        parsed: Dict[str, str] = parse_cid(cid_data)
        for k, v in parsed.items():
            print(f"{k}: {v}")
        
        print("\nUnlock Data:")
        unlock_data = get_unlock_data(parsed)
        if unlock_data:
            print(unlock_data.upper())
        else:
            print("No unlock data available.")
    
    except ValueError as e:
        print(f"Error parsing CID data: {e}")
        sys.exit(1)


    print("\nSaved certificate in current directory.")
    cert_data = cid_data[0x172:0x9C7]
    with open("cert.der", 'wb') as cert_file:
        cert_file.write(cert_data)
    #cert: Certificate = parse_certificate(cert_data)
    #print(f"Subject: {cert.subject}")

if __name__ == "__main__":
    main()

