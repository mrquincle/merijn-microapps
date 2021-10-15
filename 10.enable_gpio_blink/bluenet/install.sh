#!/bin/sh
# Has to be put in the root dir of the bluenet repo

mkdir -p build
cd build

cmake .. -DBOARD_TARGET=meri
make

#cd default
#make
#
#cd ../
make erase
make write_softdevice

make read_softdevice_version
make write_mbr_param_address

cd meri
make write_board_version

cd bootloader
make write_bootloader
make write_bootloader_address

cd ../
make write_application

make build_bootloader_settings
make write_bootloader_settings

cd ../
make reset

cd ../
