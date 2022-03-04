#!/usr/bin/env python

import argparse
import os
import subprocess
import sys

script_dir=os.path.split(os.path.realpath(__file__))[0]

def merge_bin(project_path, language):
    filename="box_lite_factory_en.bin"
    cmd="eptool.py --chip esp32s3 merge_bin -o $file --flash_mode dio --flash_size 16MB \
    0x0 $project_path/build/bootloader/bootloader.bin \
    0x20000 $project_path/build/lite_demo.bin \
    0x8000 $project_path/build/partition_table/partition-table.bin \
    0x16000 $project_path/build/ota_data_initial.bin \
    0x3bd000 $project_path/build/storage.bin \
    0x647000 $project_path/build/model.bin"

    if language == "cn":
        filename=filename.replace("_en", "_cn")

    args = [
        sys.executable,
        os.getenv('IDF_PATH')+"/components/esptool_py/esptool/esptool.py",
        "--chip",
        "esp32s3",
        "merge_bin",
        "-o",
        filename,
        "--flash_mode", 
        "dio", 
        "--flash_size",
        "16MB",
        "0x0",
        project_path+"/build/bootloader/bootloader.bin",
        "0x20000",
        project_path+"/build/lite_demo.bin",
        "0x8000",
        project_path+"/build/partition_table/partition-table.bin",
        "0x16000",
        project_path+"/build/ota_data_initial.bin",
        "0x3bd000",
        project_path+"/build/storage.bin",
        "0x647000",
        project_path+"/build/model.bin",
    ]
    if language == "cn":
        print("Merge bin for Chinese")
        args.append("0x10000")
        args.append("%s/nvs.bin" % script_dir)
    elif language == "en":
        print("Merge bin for English")
    else:
        print("language error")
        return None

    output = subprocess.check_output(args).decode('utf-8')
    return os.path.abspath(filename)

def download(port, file):
    args = [
        sys.executable,
        os.getenv('IDF_PATH')+"/components/esptool_py/esptool/esptool.py",
        "--chip",
        "esp32s3",
        "-p",
        port,
        "-b",
        "3000000",
        "--before=default_reset",
        "--after=hard_reset",
        "--no-stub",
        "write_flash",
        "--flash_mode",
        "dio",
        "--flash_freq",
        "80m",
        "--flash_size",
        "16MB",
        "0x0",
        file,
    ]
    output = subprocess.check_output(args).decode('utf-8')

if __name__ == "__main__":
    bin_file=merge_bin("/home/zhouli/Work/esp-box/examples/factory_demo", "cn")
    os.system("./multi_download.sh "+bin_file)
