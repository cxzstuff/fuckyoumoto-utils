#!/bin/bash

if [ -z "$1" ]; then
	echo "Usage: $0 <firmware_directory> <MODE (1/2)> (1 - default)"
	exit 1
fi

FIRMWARE_DIR="$1"
MODE="${2:-1}"

mode1(){
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
}

mode2(){
	./flash_stock.sh "$FIRMWARE_DIR"
}

python mtkbootcmd.py FASTBOOT

if [ "$MODE" = "1" ]; then
	mode1
elif [ "$MODE" = "2" ]; then
	mode2
fi

fastboot reboot
