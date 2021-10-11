#!/bin/sh

rm -rf ~/.platformio/platforms/cs-microapps
mkdir ~/.platformio/platforms/cs-microapps
cp -r . ~/.platformio/platforms/cs-microapps
rm ~/.platformio/platforms/cs-microapps/install.sh
