#!/usr/bin/env python3

import asyncio, aiofiles, pathlib, aiohttp
import re, json
import random

ids_map = {
    "⿰": {"k": 's', "n": 2},
    "⿱": {"k": 'd', "n": 2},
    "⿲": {"k": 't', "n": 3},
    "⿳": {"k": 'y', "n": 3},
    "⿴": {"k": 'q', "n": 2},
    "⿵": {"k": 'w', "n": 2},
    "⿶": {"k": 'e', "n": 2},
    "⿷": {"k": 'r', "n": 2},
    "⿸": {"k": 'u', "n": 2},
    "⿹": {"k": 'i', "n": 2},
    "⿺": {"k": 'o', "n": 2},
    "⿻": {"k": 'p', "n": 2},
}

py_a = ['ā', 'á', 'ǎ', 'à']
py_o = ['ō', 'ó', 'ǒ', 'ò']
py_e = ['ē', 'é', 'ě', 'è']
py_i = ['ī', 'í', 'ǐ', 'ì']
py_u = ['ū', 'ú', 'ǔ', 'ù']
py_v = ['ǖ', 'ǘ', 'ǚ', 'ǜ', 'ü']
py_n = {'ǹ', 'ń', 'ň'}
py_m = {'ḿ'}

async def drop_shengdiao(py):
    ret = ""
    sd = 1
    for c in py:
        if c in py_a:
            sd = py_a.index(c) + 1
            ret = ret + "a"
        elif c in py_o:
            sd = py_o.index(c) + 1
            ret = ret + "o"
        elif c in py_e:
            sd = py_e.index(c) + 1
            ret = ret + "e"
        elif c in py_i:
            sd = py_i.index(c) + 1
            ret = ret + "i"
        elif c in py_u:
            sd = py_u.index(c) + 1
            ret = ret + "u"
        elif c in py_v:
            sd = py_v.index(c) + 1
            if sd == 5:
                sd = 1
            ret = ret + "v"
        elif c in py_n:
            ret = ret + "n"
        elif c in py_m:
            ret = ret + "m"
        else:
            ret = ret + c
    return ret, sd

async def get_zdic_data(hz):
    if not pathlib.Path(f"./zdic_data/{hz}.txt").exists():
        # print(f"download {hz}")
        async with aiohttp.ClientSession() as session:
            async with session.request("get", f"https://www.zdic.net/hans/{hz}") as resp:
                async with aiofiles.open(f"./zdic_data/{hz}.txt", mode="w") as f:
                    await f.write(await resp.text())
    async with aiofiles.open(f"./zdic_data/{hz}.txt", mode="r") as f:
        return await f.read()

async def get_py(zdic_data, hz):
    py_list = []
    for py in zdic_data[hz]['pinyin']:
        # print(py)
        py_dropped, sd = await drop_shengdiao(py)
        # print(py_dropped)
        ret = list()
        ret.append(py_dropped[0])
        yunmu = ['a', 'o', 'e', 'i', 'u', 'v']
        if py_dropped[0] in yunmu or py[0] in py_n or py[0] in py_m:
            ret.append(py_dropped[0:])
        else:
            if py_dropped[1] != "h":
                ret.append(py_dropped[1:])
            else:
                ret.append(py_dropped[2:])
        py_list.append((ret, sd))
    return py_list

async def get_bihua(zdic_data, hz):
    return zdic_data[hz]['bihua']

async def ids_parser_inner(zd, ids_string, start):
    if ids_string[start] in ids_map:
        ret = ""
        i = start + 1
        n = ids_map[ids_string[start]]['n']
        for ii in range(n):
            bh, i = await ids_parser_inner(zd, ids_string, i)
            ret = ret + bh
        return ret, i
    else:
        return await get_bihua(zd, ids_string[start]), start + 1


async def ids_parser(zd, ids_string):
    # print(ids_string)
    ret = []
    i = 0
    if ids_string[i] in ids_map:
        n = ids_map[ids_string[i]]['n']
        k = ids_map[ids_string[i]]['k']
        i = i + 1
        for ii in range(n):
            bh, i = await ids_parser_inner(zd, ids_string, i)
            ret.append(bh)
    else:
        return ""
    # keya = await bihua_parser(ret[0][0] + ret[1][0])
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
    yunmu_stats = dict()
    zd_data = ""
    async with aiofiles.open("zdic_data.json", mode="r") as f:
        zd_data = json.loads(await f.read())

    async with aiofiles.open("ids_data/ids.txt", mode="r") as ids_file:
        count = 0
        ids_data = await ids_file.read()
        async with aiofiles.open("ty7k/words.txt", mode="r") as f:
            async for line in f:
                hz = line.strip()
                ma = re.search(r"U\S+\s+(" + hz + r")\s+([^\[\s]+)", ids_data)
                ids_string = ma.group(2)
                py_list = await get_py(zd_data, hz)
                bh_parsed = ""
                if zd_data[hz]['struct'] == "单一结构" or zd_data[hz]['struct'] == "独体字":
                    bh_parsed = "g" + (await bihua_parser(await get_bihua(zd_data, hz)))[:2]
                else:
                    try:
                        bh_parsed = await ids_parser(zd_data, ids_string)
                    except:
                        print(f'{count}: {hz} - {ids_string}')
                if bh_parsed == "":
                    bh_parsed = "g" + (await bihua_parser(await get_bihua(zd_data, hz)))[:2]
                m = set()
                py_set = set()
                yunmu_groups = [
                    {'a',  'ai',  'ao',  'ou',  'ei'},
                    {'o',  'an',  'ang', 'in',  'ing'},
                    {'e',  'en',  'eng',  'un',  'ong'},
                    {'i',  'ia',  'ie',  'iu'},
                    {'u',  'uo',  'ua',  'ui',  'ue', 've'},
                    {'v',  'iao',  'iang',  'ian',  'iong', 'uang', 'uai', 'uan'}
                ]
                for py, sd in py_list:
                    py_set.add((py[0], py[1]))
                for py in py_set:
                    py1 = py[0]
                    map_key1 = ['a', 's', 'd', 'f', 'c', 'v']
                    map_key2 = ['h', 'j', 'k', 'l', 'n', 'm']
                    if bh_parsed[0] == 's':
                        i = 5
                        for ii, g in enumerate(yunmu_groups):
                            if py[1] in g:
                                i = ii
                                break
                        m.add(py1 + map_key1[i] + bh_parsed[1:])
                    elif bh_parsed[0] == 'd':
                        i = 5
                        for ii, g in enumerate(yunmu_groups):
                            if py[1] in g:
                                i = ii
                                break
                        m.add(py1 + map_key2[i] + bh_parsed[1:])
                    else:
                        m.add(py1 + bh_parsed)

                mb_data[hz] = { 'm':  m }
                count += 1

    # print(f'{mb_data}')
    mb_stats = dict()
    async with aiofiles.open(f"./mb.txt", mode="w") as f:
        for k, v in mb_data.items():
            ms = v['m']
            for m in ms:
                if m in mb_stats:
                    mb_stats[m] += 1
                else:
                    mb_stats[m] = 1
                await f.write(f"{m} {k}\n")

    print({k: v for k, v in sorted(mb_stats.items(), key=lambda item: item[1])})
    # print({k: v for k, v in sorted(yunmu_stats.items(), key=lambda item: item[1])})
    # c = 0
    # for k, v in yunmu_stats.items():
    #     c = c + v
    # print(c)




asyncio.run(main())
