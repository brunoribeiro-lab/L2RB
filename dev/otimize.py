import cv2
import threading
import time
import numpy as np
import adbutils
import os

import asyncio
import aiofiles
from ppadb.client_async import ClientAsync as AdbClient

async def _save_screenshot(device):
    result = await device.screencap()
    file_name = f"now.png"
    async with aiofiles.open(f"{file_name}", mode='wb') as f:
        await f.write(result)

    return file_name

async def main():
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = await client.devices()
    for device in devices:
        print(device.serial)

    result = await asyncio.gather(*[_save_screenshot(device) for device in devices])
    print(result)

asyncio.run(main())

def main2():
    try:
        adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
        if len(adb.device_list()) == 0 and os.path.isfile('./now.png') == False:
            #restartL2()
            print("no connected")
            return False
        try:
            d = adb.device()
            stream = d.shell("screencap /sdcard/now.png")
            d.sync.pull("/sdcard/now.png", "now.png")  # pulling image
            #time.sleep(2)
            exists = os.path.isfile('./now.png')
            if exists == False:
                del exists
                return False
            else:
                del exists
                size = os.path.getsize("now.png")
                return False
            return True
        except IOError:
            print("Error Device not found, restarting....")
            return False
    except IOError:
        print("Error")
        return False



main2()
