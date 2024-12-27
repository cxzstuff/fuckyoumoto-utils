import os
import datetime
import re
import subprocess

import da

LOGS_BASE_DIR = "logs"
os.makedirs(LOGS_BASE_DIR, exist_ok=True)

# REGEX for clearing logs of confidential information
IMEI1_REGEX = b"info_text is ' IMEI1:\\s*([0-9]+)"
IMEI2_REGEX = b"info_text is ' IMEI2:\\s*([0-9]+)"
IMEI_PROINFO = b"imei_string from proinfo: \"\\s*([0-9]+)"
SRL_NUM_EEGEX = b"info_text is ' TRACKID:\\s*([A-Za-z0-9]+)"

def get_logs(file_name):
    output_file = os.path.join(LOGS_BASE_DIR, file_name)
    print(f"Read logs from expdb partition...")

    try:
        subprocess.run(
            ["mtk", "r", "expdb", output_file]
        )
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to read logs from expdb partition.")
        print(f"Error details: {e.stderr.decode()}")

def clean_logs(file_name):
    output_file = os.path.join(LOGS_BASE_DIR, file_name)

    with open(output_file, "rb") as f:
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

        with open(output_file, "wb") as f:
            f.write(buffer)

        print("Confidential information has been deleted!")

def main():
    # Read gpt partitions output to keep the phone in DA mode
    da.print_gpt()

    now = datetime.datetime.now()
    timestamp = now.strftime("expdb-%Y-%m-%d_%H-%M-%S")

    get_logs(timestamp)
    clean_logs(timestamp)

    print(f"Read expdb logs completed. File saved to {LOGS_BASE_DIR}/{timestamp}.")

if __name__ == "__main__":
    main()