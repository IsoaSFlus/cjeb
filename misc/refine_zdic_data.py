#!/usr/bin/env python3

import asyncio, aiofiles, pathlib, aiohttp
import re
import random, json

async def main():
    out = dict()
    zdic_files = pathlib.Path(f"./zdic_data").glob("*.txt")
    for f in zdic_files:
        async with aiofiles.open(f"{f}", mode="r") as f:
            zd = await f.read()
            ma = re.search(r'<td class="dsk_2_1">(\S+)</td>', zd)
            # print(f.name[-5])
            if not f.name[-5] in out:
                out[f'{f.name[-5]}'] = {}
            try:
                out[f'{f.name[-5]}']['struct'] = ma.group(1)
            except:
                out[f'{f.name[-5]}']['struct'] = ""
                print(f'{f.name} 没有结构信息')

            ma = re.search(r'<td align="center" class="z_bis2"><p>([0-9]+)</p></td>', zd)
            try:
                out[f'{f.name[-5]}']['bihua'] = ma.group(1)
            except:
                out[f'{f.name[-5]}']['bihua'] = ""
                print(f'{f.name} 没有笔画信息')

            try:
                ma = re.search(r'<td class="z_py"><p><span class="z_d song">.+?</td>', zd)
                ma = re.findall(
                    r'<span class="z_d song">([^<]+)<span class="ptr">', ma.group(0)
                )
                out[f'{f.name[-5]}']['pinyin'] = ma
            except:
                out[f'{f.name[-5]}']['pinyin'] = ""
                print(f'{f.name} 没有拼音信息')

    async with aiofiles.open(f"./zdic_data.json", mode="w") as f:
        await f.write(json.dumps(out, ensure_ascii=False))

asyncio.run(main())
