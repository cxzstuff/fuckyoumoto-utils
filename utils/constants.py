DEVICES: dict = {
    "penangf":
    {
        "da_files": ["DA_PL_NO_CERT_V6.bin", "MT6768_USER.bin"],
        "preloader": "preloader_penangf.bin",
        "scatter": "MT6768_Android_scatter.txt",
        "partition_scheme": "penangf_partitons.csv",
        "has_unlock_method": True,
        "preferred_da": 1,
    },
    "fogorow":
    {
        "da_files": ["DA_SWSEC_2316_p325a_dl_forbidden3.bin", "DA_SWSEC_2316_p325a.bin"],
        "preloader": "preloader_p235a.bin",
        "scatter": "MT6768_Android_scatter.txt",
        "partition_scheme": "fogorow_partitions.csv",
        "has_unlock_method": False,
        "preferred_da": 0,
    },
}
