import csv
from utils.constants import DEVICES
from utils.path import get_sources_path

class Device:
    def __init__(self, code_name: str) -> None:
        self.code_name: str = code_name
        self.da: list = DEVICES[code_name]["da_files"]
        self.preloader: str = DEVICES[code_name]["preloader"]
        self.scatter: str = DEVICES[code_name]["scatter"]
        self.partition_scheme: str = DEVICES[code_name]["partition_scheme"]
        self.preferred_da_index: int = DEVICES[code_name]["preferred_da"]

    @property
    def name(self) -> str:
        return self.code_name

    def get_preloader_path(self) -> str:
        return f"sources/{self.code_name}/{self.preloader}"
    
    def get_da_path(self, index: int) -> str:
        print(len(self.da) - 1)
        if index > len(self.da) - 1:
            index = 0
        return f"{get_sources_path()}/{self.code_name}/{self.da[index]}"

    def get_partition_scheme_as_dict(self) -> dict:
        path: str = f"{get_sources_path()}/{self.code_name}/{self.partition_scheme}"
        
        scheme: dict = {}
        with open(path, "r") as pscheme:
            reader = csv.DictReader(pscheme)

            for row in reader:
                scheme[row["Partition"]] = {"address": row["Address"], "size": row["Size"]} #"empty": row["empty"], "writable": row["writable"]}

        return scheme