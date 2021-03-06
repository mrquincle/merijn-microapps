#!/usr/bin/env python3

import json

import asyncio
import datetime

from crownstone_ble import CrownstoneBle, BleEventBus, BleTopics

import crownstone_ble
import argparse

import logging
logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s', level=logging.INFO)

def setup_parser(description):
    parser = argparse.ArgumentParser(description)
    parser.add_argument('-a', '--bleAddress', required=True, help='Crownstone Mac address')
    parser.add_argument('-f', '--file', default=None, help='Microapp binary to upload')
    parser.add_argument('-d', '--adapterAddress', default=None, help='Internal Adapter')
    parser.add_argument('-s', '--spherefile', default=None, help='Sphere keys file')
    return parser.parse_args()

args = setup_parser("Script to upload microapps via BLE")

# Load sphere keys from config file
core = CrownstoneBle(bleAdapterAddress=args.adapterAddress)
sphere = open(args.spherefile)
core.loadSettingsFromDictionary(json.load(sphere))

maxChunkSize = 192

# The index where we want to put our microapp.
appIndex = 0

async def main():

    with open(args.file, "rb") as f:
        appData = f.read()

    #print("First 32 bytes of the binary:")
    #print(list(appData[0:32]))

    await core.connect(args.bleAddress)
    info = await core._dev.getMicroappInfo()
    print(info)

    # Perform some checks with the info we received.
    if appIndex >= info.maxApps:
        print(f"This crownstone doesn't have room for index {appIndex}")
        await core.disconnect()
        await core.shutDown()
        return

    if len(appData) > info.maxAppSize:
        print(f"This crownstone doesn't have room for a binary size of {len(appData)}")
        await core.disconnect()
        await core.shutDown()
        return

    # If there is already some data at this index, it has to be removed first.
    if info.appsStatus[appIndex].tests.hasData:
        print(f"Remove data at index {appIndex}")
        await core._dev.removeMicroapp(appIndex)

    # Determine the chunk size by taking the minimum of our max, and the crownstones max.
    chunkSize = min(maxChunkSize, info.maxChunkSize)

    print(f"{datetime.datetime.now()} Start upload with chunkSize={chunkSize}")
    await core._dev.uploadMicroapp(appData, appIndex, chunkSize)
    print(f"{datetime.datetime.now()} Upload done")

    print("Validate..")
    await core._dev.validateMicroapp(appIndex)
    print("Validate done")

    print("Enable..")
    await core._dev.enableMicroapp(appIndex)
    print("Enable done")

    await core.disconnect()
    await core.shutDown()

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
except KeyboardInterrupt:
    print("Stopping.")
