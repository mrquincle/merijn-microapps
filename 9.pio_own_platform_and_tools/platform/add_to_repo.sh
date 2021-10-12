#!/bin/bash

#mkdir ~/.piorepos
cp -r platform-csmicroapps ~/.piorepos/

cd ~/.piorepos/platform-csmicroapps/
git add -A
git commit -m "..."
git push
