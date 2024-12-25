import re
import sys

args = sys.argv

if len(args) < 2:
    print("Usage: python3 clean_logs.py <log file>")
    sys.exit(0)

log_file = args[1]

IMEI1_REGEX = b"info_text is ' IMEI1:\\s*([0-9]+)"
IMEI2_REGEX = b"info_text is ' IMEI2:\\s*([0-9]+)"
IMEI_PROINFO = b"imei_string from proinfo: \"\\s*([0-9]+)"
SRL_NUM_EEGEX = b"info_text is ' TRACKID:\\s*([A-Za-z0-9]+)"

with open(log_file, "rb") as f:
    buffer = f.read()
    buffer = buffer.strip(b'\x00') # Strips empty bytes from (Which takes almost all the file size)
    
    # This makes sure we get rid of every empty byte within the logs themselves
    buffer = buffer.replace(b'\x00', b'')

    # Clean Sensitive data from logs
    match = re.search(IMEI1_REGEX, buffer)
    if match:
        imei1 = match.group(1)
        buffer = buffer.replace(imei1, b'IMEI1_REDACTED')
    else:
        match = re.search(IMEI_PROINFO, buffer)
        if match:
            imei1 = match.group(1)
            buffer = buffer.replace(imei1, b'IMEI_REDACTED')

    match = re.search(IMEI2_REGEX, buffer)
    if match:
        imei2 = match.group(1)
        buffer = buffer.replace(imei2, b'IMEI2_REDACTED')
    else:
        match = re.search(IMEI_PROINFO, buffer, re.MULTILINE)
        if match:
            imei2 = match.group(1)
            buffer = buffer.replace(imei2, b'IMEI_REDACTED')
    
    match = re.search(SRL_NUM_EEGEX, buffer)
    if match:
        srl = match.group(1)
        buffer = buffer.replace(srl, b'SRL_REDACTED')



with open(log_file, "wb") as f:
    f.write(buffer)

print("Logs cleaned!")
