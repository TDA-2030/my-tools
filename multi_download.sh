#!/bin/bash
set -e
set -u

uarts=($(ls -a /dev/ttyACM*))
script_dir=$(cd $(dirname $0);pwd)
project_path=/home/zhouli/Work/esp-box/examples/factory_demo

echo "============================="
echo "deveice num sum: ${#uarts[@]}"
echo "project path: $project_path"
echo "============================="

erase(){
    esptool.py -p $1 erase_flash
}

combine(){
if $1
then #Chinese
    echo "Merge bin for Chinese"
    eptool.py --chip esp32s3 merge_bin -o $2 --flash_mode dio --flash_size 16MB \
    0x0 $project_path/build/bootloader/bootloader.bin \
    0x10000 $script_dir/nvs.bin \
    0x20000 $project_path/build/lite_demo.bin \
    0x8000 $project_path/build/partition_table/partition-table.bin \
    0x16000 $project_path/build/ota_data_initial.bin \
    0x3bd000 $project_path/build/storage.bin \
    0x647000 $project_path/build/model.bin
else # English
    echo "Merge bin for English"
    esptool.py --chip esp32s3 merge_bin -o $2 --flash_mode dio --flash_size 16MB \
    0x0 $project_path/build/bootloader/bootloader.bin \
    0x20000 $project_path/build/lite_demo.bin \
    0x8000 $project_path/build/partition_table/partition-table.bin \
    0x16000 $project_path/build/ota_data_initial.bin \
    0x3bd000 $project_path/build/storage.bin \
    0x647000 $project_path/build/model.bin
fi
}

download_one_bin(){
    esptool.py --chip esp32s3 -p $1 -b 3000000 --before=default_reset --after=hard_reset --no-stub write_flash --flash_mode dio --flash_freq 80m --flash_size 16MB \
    0x0 $2
}

multi_download(){
    for i in "${!uarts[@]}"
    do
    {
        port=${uarts[i]}
        echo "downloading file $1 to $port"
        {
            # erase $port
            # download $port
            download_one_bin $port $1

        }>/dev/null

        rst_arr[$i]="$?"
        rst=$[rst_arr[$i]]
        if [ "$rst" == "0" ];then
        echo "============= download success $port ============="
        else
        echo "XXXXXXXXXXXXXX  download fail $port  XXXXXXXXXXXXX"
        fi
    }&
    done
    wait
}


multi_download $1
