import discord
import os
from dotenv import load_dotenv
from fun import songs

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

for f in os.listdir("cogs"): #列出cogs下的檔案
    if f.endswith(".py"):
        bot.load_extension(f"cogs.{f[:-3]}") #去掉.py載入檔案
        print(f"完成載入{f}")

bot.run(os.getenv("DISCORD_TOKEN")) #登入到Discord