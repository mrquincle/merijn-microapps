#!/bin/sh
#python3 upload_microapp.py -a FD:FC:93:F8:97:BA -f ./crownstone-microapp/build/example.bin
systemctl restart bluetooth
sleep 1
python3 upload_microapp.py -a FD:FC:93:F8:97:BA -f ./scons/main.bin
