#!/bin/bash

# Path to Preloader, loader
PRELOADER="./sources/preloader_penangf.bin"
LOADER="./sources/MT6768_USER.bin"

# Backup out dir
BACKUP_DIR="backups"
mkdir -p "$BACKUP_DIR"

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

# backup partiotion create command
backup_partition() {
    local partition="$1"
    local output_file="$BACKUP_DIR/${partition}.img"
    echo "Backup partition - [$partition]"
    mtk r "$partition" "$output_file" --preloader "$PRELOADER" --loader "$LOADER"
    if [[ $? -ne 0 ]]; then
        echo "Error: Failed to create partition backup $partition."
    else
        echo "Backup of $partition successfully saved to $output_file."
    fi
}

# run backup all partitions
for partition in "${PARTITIONS[@]}"; do
    backup_partition "$partition"
done

echo "Backup completed. All files saved to $BACKUP_DIR."