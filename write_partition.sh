#!/bin/bash

# Path to Preloader, loader
PRELOADER="./sources/preloader_penangf.bin"
LOADER="./sources/MT6768_USER.bin"

if [[ ! -f "$PRELOADER" ]]; then
    echo "Error: Preloader file not found at $PRELOADER"
    exit 1
fi

if [[ ! -f "$LOADER" ]]; then
    echo "Error: Loader file not found at $LOADER"
    exit 1
fi

echo "Enter partition name: "
read p_name

echo "Enter path to file: "
read file_path

if [[ ! -f "$file_path" ]]; then
    echo "Error: File not found at $file_path"
    exit 1
fi

mtk w "$p_name" "$file_path" --preloader "$PRELOADER" --loader "$LOADER"

if [[ $? -eq 0 ]]; then
    echo "Write data successful for partition $p_name"
else
    echo "Error: Failed to write partition $p_name"
    exit 1
fi
