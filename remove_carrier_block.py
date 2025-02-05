import subprocess
#import da

ELABLE_PATH="./sources/penangf/unlock_elable.img"

def unlock_elable():
    try:
        subprocess.run(["mtk", "w", "elable", ELABLE_PATH
            , "--preloader", "./sources/penangf/preloader_penangf.bin"
            , "--loader", "./sources/penangf/MT6768_USER.bin"
        ], check=True)

        print("Carrier unlocked successfully.")

    except subprocess.CalledProcessError as e:
        print("Error while unlocking carrier.")
        print(f"Error details: {e.strerr.decode()}")

def main():
    # da.print_gpt()

    unlock_elable()

if __name__ == "__main__":
    main()
