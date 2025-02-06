from utils.device import Device
from utils.mtkclient_wrapper import MTKClientWrapper
import sys

def perform_dump(device: Device, include_super: bool) -> None:
    mtkclient_wrapper = MTKClientWrapper(device)

    mtkclient_wrapper.perform_full_dump(include_super)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 full_dump.py <device-name>")
        print("Optional arguments: --include-super --- Dump super partition ")
        sys.exit(1)

    device = Device(sys.argv[1])
    if len(sys.argv) > 2:
        if sys.argv[2] == "--include-super":
            perform_dump(device, True)
    else:
        perform_dump(device, False)