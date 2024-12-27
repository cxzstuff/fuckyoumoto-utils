import os
import datetime
import subprocess

import da

LOGS_BASE_DIR = "logs"
os.makedirs(LOGS_BASE_DIR, exist_ok=True)

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

def main():
    # Read gpt partitions output to keep the phone in DA mode
    da.print_gpt()

    now = datetime.datetime.now()
    timestamp = now.strftime("expdb-%Y-%m-%d_%H-%M-%S")

    get_logs(timestamp)

    print(f"Read expdb logs completed. File saved to {LOGS_BASE_DIR}/{timestamp}.")

if __name__ == "__main__":
    main()