#!/bin/sh
systemctl restart bluetooth
sleep 1
cd scons
scons -c
scons

cd ../
python3 upload_microapp.py -a FD:FC:93:F8:97:BA -f ./scons/main.bin
