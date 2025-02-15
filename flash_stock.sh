#!/bin/bash
set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <firmware_directory>"
    exit 1
fi

FIRMWARE_DIR="$1"

if [ ! -d "$FIRMWARE_DIR" ]; then
    echo "Error: Directory '$FIRMWARE_DIR' does not exist."
    exit 1
fi

echo ""
echo "[STEP] Flashing the all vbmeta"
echo ""

fastboot flash --disable-verity --disable-verification vbmeta "$FIRMWARE_DIR/vbmeta.img"
fastboot flash --disable-verity --disable-verification vbmeta_system "$FIRMWARE_DIR/vbmeta_system.img"
fastboot flash --disable-verity --disable-verification vbmeta_vendor "$FIRMWARE_DIR/vbmeta_vendor.img"

echo ""
echo "[STEP] Flashing the bootloader"
echo ""

fastboot flash lk "$FIRMWARE_DIR/lk.img"
fastboot reboot bootloader

echo ""
echo "[WARNING] The phone will reboot into bootloader mode, there may be no image on the screen, just wait until the process is complete"
echo "[WARNING] The phone will reboot into bootloader mode, there may be no image on the screen, just wait until the process is complete"
echo "[WARNING] The phone will reboot into bootloader mode, there may be no image on the screen, just wait until the process is complete"
echo ""

echo ""
echo "[STEP] Flashing boot"
echo ""
fastboot flash boot "$FIRMWARE_DIR/boot.img"

if [ -f "$FIRMWARE_DIR/vendor_boot.img" ]; then
    echo ""
    echo "[STEP] Flashing vendor_boot"
    echo ""
    fastboot flash vendor_boot "$FIRMWARE_DIR/vendor_boot.img"
else
    echo "[INFO] vendor_boot.img not found, skipping..."
fi

echo ""
echo "[STEP] Flashing all other partitions"
echo ""

fastboot flash md1img "$FIRMWARE_DIR/md1img.img"
fastboot flash scp "$FIRMWARE_DIR/scp.img"
fastboot flash spmfw "$FIRMWARE_DIR/spmfw.img"
fastboot flash sspm "$FIRMWARE_DIR/sspm.img"
fastboot flash dtbo "$FIRMWARE_DIR/dtbo.img"
fastboot flash gz "$FIRMWARE_DIR/gz.img"
fastboot flash tee "$FIRMWARE_DIR/tee.img"

fastboot flash super "$FIRMWARE_DIR/super.img"

echo ""
echo "[STEP] Erasing userdata/metadata"
echo ""

fastboot erase userdata
fastboot erase metadata
fastboot erase md_udc

echo ""
echo "Flashing completed successfully!"
echo ""

fastboot reboot
