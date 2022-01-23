#!/usr/bin/env python3

import asyncio, aiofiles, pathlib, aiohttp
import re

ids_map = {
    "⿰": {"k": 's', "n": 2},
    "⿱": {"k": 'd', "n": 2},
    "⿲": {"k": 'j', "n": 3},
    "⿳": {"k": 'k', "n": 3},
    "⿴": {"k": 'l', "n": 2},
    "⿵": {"k": 'w', "n": 2},
    "⿶": {"k": 'e', "n": 2},
    "⿷": {"k": 'r', "n": 2},
    "⿸": {"k": 'u', "n": 2},
    "⿹": {"k": 'i', "n": 2},
    "⿺": {"k": 'o', "n": 2},
    "⿻": {"k": 'f', "n": 2},
}

py_a = {'ā', 'á', 'ǎ', 'à'}
py_o = {'ō', 'ó', 'ǒ', 'ò'}
py_e = {'ē', 'é', 'ě', 'è'}
py_n = {'ǹ', 'ń', 'ň'}

async def get_zdic_data(hz):
    if not pathlib.Path(f"./zdic_data/{hz}.txt").exists():
        # print(f"download {hz}")
        async with aiohttp.ClientSession() as session:
            async with session.request("get", f"https://www.zdic.net/hans/{hz}") as resp:
                async with aiofiles.open(f"./zdic_data/{hz}.txt", mode="w") as f:
                    await f.write(await resp.text())
    async with aiofiles.open(f"./zdic_data/{hz}.txt", mode="r") as f:
        return await f.read()

async def get_py(zdic_data):
    ma = re.search(
        r'<td class="z_py"><p><span class="z_d song">([^<]+)<span class="ptr">', zdic_data
    )
    py = ma.group(1)
    if py[0] in py_a:
        py = "a"
    elif py[0] in py_o:
        py = "o"
    elif py[0] in py_e:
        py = "e"
    elif py[0] in py_n:
        py = "n"
    return py[0]

async def get_bihua(zdic_data):
    ma = re.search(r'<td align="center" class="z_bis2"><p>([0-9]+)</p></td>', zdic_data)
    bihua = ma.group(1)
    return bihua


async def ids_parser_inner(ids_string, start):
    if ids_string[start] in ids_map:
        ret = ""
        i = start + 1
        n = ids_map[ids_string[start]]['n']
        for ii in range(n):
            bh, i = await ids_parser_inner(ids_string, i)
            ret = ret + bh
        return ret, i
    else:
        zdata = await get_zdic_data(ids_string[start])
        return await get_bihua(zdata), start + 1


async def ids_parser(ids_string):
    # print(ids_string)
    ret = []
    i = 0
    if ids_string[i] in ids_map:
        n = ids_map[ids_string[i]]['n']
        k = ids_map[ids_string[i]]['k']
        i = i + 1
        for ii in range(n):
            bh, i = await ids_parser_inner(ids_string, i)
            ret.append(bh)
    else:
        return ""

    keya = await bihua_parser(ret[0])
    keyb = await bihua_parser(ret[1])

    return k + keya[0] + keyb[0]


async def bihua_parser(bihua_string):
    ret = ""
    tmp = ""
    for bh in bihua_string:
        tmp = tmp + bh
        if len(tmp) == 2:
            if tmp == "11":
                ret = ret + "h"
            elif tmp == "12":
                ret = ret + "j"
            elif tmp == "13":
                ret = ret + "k"
            elif tmp == "14":
                ret = ret + "l"
            elif tmp == "15":
                ret = ret + "m"
            elif tmp == "21":
                ret = ret + "a"
            elif tmp == "22":
                ret = ret + "s"
            elif tmp == "23":
                ret = ret + "d"
            elif tmp == "24":
                ret = ret + "f"
            elif tmp == "25":
                ret = ret + "g"
            elif tmp == "31":
                ret = ret + "q"
            elif tmp == "32":
                ret = ret + "w"
            elif tmp == "33":
                ret = ret + "e"
            elif tmp == "34":
                ret = ret + "r"
            elif tmp == "35":
                ret = ret + "t"
            elif tmp == "41":
                ret = ret + "y"
            elif tmp == "42":
                ret = ret + "u"
            elif tmp == "43":
                ret = ret + "i"
            elif tmp == "44":
                ret = ret + "o"
            elif tmp == "45":
                ret = ret + "p"
            elif tmp == "51":
                ret = ret + "z"
            elif tmp == "52":
                ret = ret + "x"
            elif tmp == "53":
                ret = ret + "c"
            elif tmp == "54":
                ret = ret + "v"
            elif tmp == "55":
                ret = ret + "b"
            tmp = ""

    if tmp == "1":
        ret = ret + "z"
    elif tmp == "2":
        ret = ret + "x"
    elif tmp == "3":
        ret = ret + "c"
    elif tmp == "4":
        ret = ret + "v"
    elif tmp == "5":
        ret = ret + "b"
    return ret


async def main():
    mb_data = dict()
    async with aiofiles.open("ids_data/ids.txt", mode="r") as ids_file:
        count = 0
        ids_data = await ids_file.read()
        async with aiofiles.open("ty7k/words.txt", mode="r") as f:
            async for line in f:
                hz = line.strip()
                ma = re.search(r"U\S+\s+(" + hz + r")\s+([^\[\s]+)", ids_data)
                # print(f'{ma.group(1)}-{ma.group(2)}')
                ids_string = ma.group(2)
                zd_data = await get_zdic_data(hz)
                py = await get_py(zd_data)
                bh_parsed = ""
                ma = re.search(r'<td class="dsk_2_1">(\S+)</td>', zd_data)
                if ma.group(1) == "单一结构" or ma.group(1) == "独体字":
                    bh_parsed = "n" + (await bihua_parser(await get_bihua(zd_data)))[:2]
                else:
                    try:
                        bh_parsed = await ids_parser(ids_string)
                    except:
                        print(f'{count}: {hz} - {ids_string}')
                if bh_parsed == "":
                    continue
                mb_data[f'{hz}'] = { 'm':  py[0] + bh_parsed }
                count += 1

    # print(f'{mb_data}')
    async with aiofiles.open(f"./mb.txt", mode="w") as f:
        for k, v in mb_data.items():
            m = v['m']
            await f.write(f"{m} {k}\n")


asyncio.run(main())
