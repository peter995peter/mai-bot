import discord
import os
from dotenv import load_dotenv
from fun import songs
import asyncio
import itertools

if not os.path.exists("data"): #初次啟動
    os.makedirs("data")
    os.makedirs("data/cache")
    with open("data/link.json", "w") as file:
        file.write("{}")
    with open("data/page.json", "w") as file:
        file.write("{}")
    songs.update()

load_dotenv() #讀取.env

bot = discord.Bot()

@bot.event
async def on_ready(): #完成Discord登入時通知
    print(bot.user)
    sl = itertools.cycle([
        f"在{len(bot.guilds)}個伺服器",
        "maimaiでらっくす",
        "舞萌",
        "舞萌DX",
        "舞萌DX 2021",
        "舞萌DX 2022",
        "舞萌DX 2023",
        "舞萌DX 2024",
        "舞萌DX 2025",
        "maimai",
        "maimai PLUS",
        "maimai GreeN",
        "maimai GreeN PLUS",
        "maimai ORANGE",
        "maimai ORANGE PLUS",
        "maimai PiNK",
        "maimai PiNK PLUS",
        "maimai MURASAKi",
        "maimai MURASAKi PLUS",
        "maimai MiLK",
        "maimai MiLK PLUS",
        "maimai FiNALE",
        "maimai DX",
        "maimai DX PLUS",
        "maimai DX Splash",
        "maimai DX Splash PLUS",
        "maimai DX UNiVERSE",
        "maimai DX UNiVERSE PLUS",
        "maimai DX FESTiVAL",
        "maimai DX FESTiVAL PLUS",
        "maimai DX BUDDiES",
        "maimai DX BUDDiES PLUS",
        "maimai DX PRiSM",
        "maimai DX PRiSM PLUS",
        "maimai DX CiRCLE",
        "maimai DX CiRCLE PLUS"
        ])
    while True:
        await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name=f"/help | {next(sl)}"))
        await asyncio.sleep(30)

for f in os.listdir("cogs"): #列出cogs下的檔案
    if f.endswith(".py"):
        bot.load_extension(f"cogs.{f[:-3]}") #去掉.py載入檔案
        print(f"完成載入{f}")

bot.run(os.getenv("DISCORD_TOKEN")) #登入到Discord