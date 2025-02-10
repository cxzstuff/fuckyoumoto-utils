#!/bin/bash

# Variables representing paths to Preloader, loader
PRELOADER="./sources/penangf/preloader_penangf.bin"
LOADER="./sources/penangf/MT6768_USER.bin"

# Backup output directory (where to save backup files)
BACKUP_DIR="backups"
mkdir -p "$BACKUP_DIR"

# List of partitions to be backed up
PARTITIONS=(
    "misc"
    "para"
    "expdb"
    "frp"
    "hw"
    "utags"
    "utagsBackup"
    "vbmeta_a"
    "vbmeta_system_a"
    "vbmeta_vendor_a"
    "vbmeta_b"
    "vbmeta_system_b"
    "vbmeta_vendor_b"
    "md_udc"
    "metadata"
    "nvcfg"
    "nvdata"
    "persist"
    "protect1"
    "protect2"
    "seccfg"
    "md1img_a"
    "spmfw_a"
    "scp_a"
    "sspm_a"
    "gz_a"
    "lk_a"
    "boot_a"
    "vendor_boot_a"
    "dtbo_a"
    "tee_a"
    "sec1"
    "proinfo"
    "boot_para"
    "nvram"
    "rfcal"
    "cid"
    "sp"
    "elable"
    "prodper"
    "kpan"
    "flashinfo"
)

# Displays the status of partition backups and informs about errors, also puts files in the backup directory
backup_partition() {
    local partition="$1"
    local output_file="$BACKUP_DIR/${partition}.img"
    echo "Backing up partition - [$partition]"
    mtk r "$partition" "$output_file" --preloader "$PRELOADER" --loader "$LOADER"
    if [[ $? -ne 0 ]]; then
        echo "Error: Failed to create partition $partition backup."
    else
        echo "Backup of $partition successfully saved to $output_file."
    fi
}

# Run the backup payload for all listed partitions
for partition in "${PARTITIONS[@]}"; do
    backup_partition "$partition"
done

echo "Backup completed. All files have been saved to the $BACKUP_DIR backup directory."
