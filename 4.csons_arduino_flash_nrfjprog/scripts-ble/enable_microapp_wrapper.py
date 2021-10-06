#!/usr/bin/env python3

Import("env")

import subprocess
from time import sleep

def before_upload(source, target, env):
    print("before_upload")

def after_upload(source, target, env):
    print('enabling microapp on crownstone...')

    # TODO Try catch something in that script to handle an error if its not working
    subprocess.run(["./scripts/enable_microapp.py", "-a", "FD:FC:93:F8:97:BA"])

env.AddPreAction("upload", before_upload)
env.AddPostAction("upload", after_upload)
