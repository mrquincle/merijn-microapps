#!/bin/bash

#mkdir ~/.piorepos
cp -r tool-cs-ble-uploader ~/.piorepos/

cd ~/.piorepos/tool-cs-ble-uploader/
git add -A
git commit -m "..."
git push
