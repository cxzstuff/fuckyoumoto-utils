import csv
import os
import sys
import subprocess
from utils.device import Device
from utils.path import get_sources_path, get_root_path
from shutil import which
from typing import Union, List


class MTKClientWrapper:
    def __init__(self, device) -> None:
        self.device: Device = device
    

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

    def perform_full_dump(self, include_super: bool) -> None:
        if self.device.partition_scheme == "":
            print("Cannot perform full dump on this device.")
            return

        print("STARTING FULL DUMP")
        dump_path: str = f"{get_root_path()}/dump/{self.device.code_name}/"
        os.makedirs(os.path.dirname(dump_path.replace(self.device.code_name, "")), exist_ok=True)
        os.makedirs(os.path.dirname(dump_path), exist_ok=True)
        

        for pname, data in self.device.get_partition_scheme_as_dict().items():
            if not include_super and pname == "super" or pname == "userdata":
                continue
            # with open(f"{dump_path}/{pname}.bin", "wb"):
            #     pass

            self.call_mtk_client("ro", data["address"], data["size"], f"{dump_path}{pname}.bin", use_loader=True)

        self.call_mtk_client("reset")
        print("FULL DUMP DONE")
