#!/bin/bash

PRELOADER="./sources/preloader_penangf.bin"
LOADER="./sources/MT6768_USER.bin"


LOGS_DIR="exported_logs"
mkdir -p "$LOGS_DIR"

echo "Reading logs.."
current_time=$(date "+%d_%m_%Y-%H:%M:%S")
mtk r expdb exported_logs/logs-$current_time.txt --loader "$LOADER" --preloader "$PRELOADER"
python3 clean_logs.py exported_logs/logs-$current_time.txt

echo "Logs saved to $LOGS_DIR/logs-$current_time"
