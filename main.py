import discord
import datetime
import json
import requests
import aiohttp
import asyncio
import tabulate
import html
import re
from discord.ext import commands
from datetime import datetime
from bs4 import BeautifulSoup
from aiofile import AIOFile

client = commands.Bot(command_prefix='.')
client.remove_command('help')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
}


@client.event
async def on_ready():
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))
    print('Bot is Running....')


@client.command()
async def kalenderakademik(ctx):
    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://47.254.238.244/kalenderakademik', headers=headers) as resp:
            status = resp.status
            if status == 200:
                js = await resp.json()

    if status == 200:
        rez = []
        for key, value in js["data"].items():
            rez.append(f"**{key}**")
            rez2 = []
            for v1, v2 in chunks(value, 2):
                rez2.append(f"{v2.replace('&ndash;','-')}: {v1}")
            rez.extend(rez2)
        result_plain = "\n".join(rez)
        embed = discord.Embed(
            title=':book: Kalender Akademik',
            colour=discord.Color.green(),
            description=f'''{result_plain}''')
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)
        return
    else:
        embed = discord.Embed(
            title=':x: Error!',
            colour=discord.Color.red(),
            description=f'Cek Kembali Commandnya! Jika diyakinkan benar maka ada kemungkinan server down.')
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)
        return


@client.command()
async def jadkul(ctx, oid):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://baak.gunadarma.ac.id/jadwal/cariJadKul', headers=headers, params={'teks': oid}) as resp:
            status = resp.status
            if status == 200:
                text = await resp.text()

    if status == 200:
        r1 = re.search(r"(.*?)<\/table>", text, re.S)
        r = re.findall(
            r"<tr.*?>.*?<td.*?>([^<]*?)</td>.*?<td.*?>([^<]*?)</td>.*?<td.*?>([^<]*?)</td>.*?<td.*?>([^<]*?)</td>.*?<td.*?>([^<]*?)</td>.*?<td.*?>([^<]*?)</td>.*?<td.*?>([^<]*?)</td>", r1.group(1), re.S)
        result = []
        for row in r:
            result.append(", ".join(map(html.unescape, row)))
        result_plain = "\n".join(result)
        embed = discord.Embed(
            title=':book: Jadwal Kuliah',
            colour=discord.Color.green(),
            description=f'''{result_plain}''')
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)
        return
    else:
        embed = discord.Embed(
            title=':x: Error!',
            colour=discord.Color.red(),
            description=f'Cek Kembali Commandnya! Jika diyakinkan benar maka ada kemungkinan server down.')
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)
        return


@client.command()
async def mhsbaru(ctx, oid):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://baak.gunadarma.ac.id/cariMhsBaru', headers=headers, params={"teks": oid, "tipeMhsBaru": "Kelas"}) as resp:
            status = resp.status
            if status == 200:
                text = await resp.text()

    if status == 200:
        r1 = re.search(r"(.*?)<\/table>", text, re.S)
        r = re.findall(
            r"<tr.*?>.*?<td.*?>([^<]*?)<\/td>.*?<td.*?>([^<]*?)<\/td>.*?<td.*?>([^<]*?)<\/td>.*?<td.*?>([^<]*?)<\/td>.*?<td.*?>([^<]*?)<\/td>.*?<td.*?>([^<]*?)<\/td>", r1.group(1), re.S)
        result = []
        for row in r:
            result.append(", ".join(map(html.unescape, row)))
        result_plain = "\n".join(result)

        embed = discord.Embed(
            title=':book: Info Mahasiswa Baru',
            colour=discord.Color.green(),
            description=f'''{result_plain}''')
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)
        return
    else:
        embed = discord.Embed(
            title=':x: Error!',
            colour=discord.Color.red(),
            description=f'Cek Kembali Commandnya! Jika diyakinkan benar maka ada kemungkinan server down.')
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)
        return


@client.command()
async def kelasbaru(ctx, oid):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://47.254.238.244/kelasbaru/kelas/{oid}', headers=headers) as resp:
            status = resp.status
            if status == 200:
                js = await resp.json()

    if status == 200:
        embed = discord.Embed(
            title=':book: Info Mahasiswa Kelas 2 Baru',
            colour=discord.Color.green(),
            description=f'''{js['data']}''')
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)
        return
    else:
        embed = discord.Embed(
            title=':x: Error!',
            colour=discord.Color.red(),
            description=f'Cek Kembali Commandnya! Jika diyakinkan benar maka ada kemungkinan server BAAK sedang Down.')
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)
        return


@client.command()
async def help(ctx):
    embed = discord.Embed(
        title='All Commands',
        colour=discord.Color.green(),
        description=f'''
.kalenderakademik - Info Kalender Akademik
.jadkul (Kelas) - Cek Jadwal Kuliah
.mhsbaru (Nama) - Info Mahasiswa Baru
.kelasbaru (Kelas) - Info Mahasiswa Kelas 2 Baru
''')
    embed.timestamp = datetime.utcnow()
    await ctx.send(embed=embed)

client.run('OTYwNTYzNzgzMjIxMjY4NTIw.GPP4kg._Z1y16u86Yah4U96BOhlf0wRfKE8JrPwlWw36Q')
