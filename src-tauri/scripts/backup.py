import os
import datetime
import subprocess

import da

BACKUP_BASE_DIR = "backups"
os.makedirs(BACKUP_BASE_DIR, exist_ok=True)

PARTITIONS = [
    "misc", "para", "expdb", "frp", "hw", "utags", "utagsBackup", "vbmeta_a", "vbmeta_system_a",
    "vbmeta_vendor_a", "vbmeta_b", "vbmeta_system_b", "vbmeta_vendor_b", "md_udc", "metadata",
    "nvcfg", "nvdata", "persist", "protect1", "protect2", "seccfg", "md1img_a", "spmfw_a", "scp_a",
    "sspm_a", "gz_a", "lk_a", "boot_a", "vendor_boot_a", "dtbo_a", "tee_a", "sec1", "proinfo",
    "boot_para", "nvram", "rfcal", "cid", "sp", "elable", "prodper", "kpan", "flashinfo"
]

def backup_partition(partition, backup_dir):
    output_file = os.path.join(backup_dir, f"{partition}.img")
    print(f"Backup partition - [{partition}]")  # Эту строку можно удалить, если не нужно

    try:
        subprocess.run(
        ["mtk", "r", partition, output_file],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to create partition backup {partition}.")
        print(f"Error details: {e.stderr.decode()}")

# Основная функция
def main():
    # Read gpt partitions output to keep the phone in DA mode
    da.print_gpt()

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = os.path.join(BACKUP_BASE_DIR, timestamp)

    # Creating a directory for backups with the current date and time
    os.makedirs(backup_dir, exist_ok=True)

    for partition in PARTITIONS:
        backup_partition(partition, backup_dir)

    print(f"Backup completed. All files saved to {backup_dir}.")

if __name__ == "__main__":
    main()