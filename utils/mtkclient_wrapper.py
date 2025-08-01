from genericpath import exists
import csv
import os
import sys
import subprocess
from utils.device import Device
from utils.path import get_sources_path, get_root_path
from shutil import which
from typing import Union, List
from pathlib import Path


class MTKClientWrapper:
    def __init__(self, device) -> None:
        self.device: Device = device
        self.dump_path: str = f"{get_root_path()}/dump/{self.device.code_name}/"
        self.partitions = self.device.get_partition_scheme_as_dict()


    def is_mtk_client_installed(self) -> bool:
        return which("mtk") != None


    @property
    def mtk_client_path(self) -> Union[str, None]:
        return which("mtk")

    def call_mtk_client(self, cmd: str, *args, **kwargs) -> None:
        if not self.is_mtk_client_installed():
            print("MTK client not found in PATH.")
            sys.exit(1)

        if cmd == "":
            print("No command specified.")
            return

        command: List = [self.mtk_client_path]
        command.extend(cmd.split(" "))
        command.extend(args)

        if kwargs.get("use_loader", False):
            command.extend(["--preloader", self.device.get_preloader_path(), "--loader", self.device.get_da_path(self.device.preferred_da_index)])

        subprocess.run(command, check=True, shell=False)

    def prepare_dirs(self):
        dump_dir = Path(os.path.dirname(self.dump_path))
        if dump_dir.exists():
            [file.unlink() for file in dump_dir.iterdir() if file.is_file()]
        else:
            os.makedirs(os.path.dirname(self.dump_path.replace(self.device.code_name, "")), exist_ok=True)
            os.makedirs(os.path.dirname(self.dump_path), exist_ok=True)

    def perform_full_dump(self, include_super: bool) -> None:
        if self.device.partition_scheme == "":
            print("Cannot perform full dump on this device.")
            return

        print("STARTING FULL DUMP")
        self.prepare_dirs()

        for pname, data in self.partitions.items():
            if not include_super and pname == "super" or pname == "userdata":
                continue
            # with open(f"{dump_path}/{pname}.bin", "wb"):
            #     pass
            parttype: str = "user"
            if pname == "preloader":
                parttype = "boot1"

            self.call_mtk_client(
                "ro",
                data["address"],
                data["size"],
                f"{self.dump_path}{pname}.bin",
                "--parttype", parttype,
                use_loader=True
            )

        self.call_mtk_client("reset")
        print("FULL DUMP DONE")

    def perform_preloaders_dump(self):
        self.prepare_dirs()

        if not "preloader" in self.partitions:
            print("error")
            exit(1)

        part_info = self.partitions["preloader"]

        files = [
            "preloader_a",
            "preloader_b"
        ]

        for file in files:
            parttype = "boot1" if file.endswith("_a") else "boot2"
            self.call_mtk_client(
                "ro",
                part_info["address"],
                part_info["size"],
                f"{self.dump_path}{file}.bin",
                "--parttype", parttype,
                use_loader=True
            )

            with open(f"{self.dump_path}{file}.bin", "rb") as f:
                data = f.read()

            with open(f"{self.dump_path}{file}.hex", "w") as f:
                f.write(data.hex())
