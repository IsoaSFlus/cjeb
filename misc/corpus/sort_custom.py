#!/usr/bin/env python3

import asyncio, aiofiles, pathlib, aiohttp
import re, json, traceback
import random

async def run():
    words_dict1 = dict()
    words_out = list()
    async with aiofiles.open("words100000.txt", mode="r") as f:
        ma = re.findall(r"(\S{2,4})\s[a-z]+\s", await f.read())
        rate = 1000000
        for cizu in ma:
            words_dict1[cizu] = rate
            rate -= 1

    async with aiofiles.open("words_custom.txt", mode="r") as f:
        # ma = re.findall(r"(\S{2,4})", await f.read())
        for cizu in await f.readlines():
            cizu = cizu.strip()
            if len(cizu) < 2 or len(cizu) > 4:
                continue
            try:
                words_out.append((cizu, words_dict1[cizu]))
            except:
                # print(f"not found {cizu}")
                words_out.append((cizu, 1))

    for cizu, rate in sorted(words_out, key=lambda item: item[1], reverse=True):
        print(cizu)

asyncio.run(run())
