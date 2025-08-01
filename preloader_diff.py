from utils.device import Device
from utils.mtkclient_wrapper import MTKClientWrapper
import sys

def diff():
    with open(f"{mtkclient_wrapper.dump_path}preloader_a.hex", "rb") as f1, open(f"{mtkclient_wrapper.dump_path}preloader_b.hex", "rb") as f2:
        data_a = f1.read()
        data_b = f2.read()

    print("\n== DIFF RESULT ==")
    if data_a == data_b:
        print("[OK] Both preloader slots are identical")
    else:
        print("[WARNING] Both preloader slots are not the identical")
        print("DO NOT ATTEMPT TO CHANGE SLOTS VIA FASTBOOT/RECOVERY, OR YOUR DEVICE WILL END UP IN A HARD BRICK STATE")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 preloader_diff.py <device-name>")
        sys.exit(1)

    device = Device(sys.argv[1])
    mtkclient_wrapper = MTKClientWrapper(device)

    mtkclient_wrapper.perform_preloaders_dump()
    diff()
