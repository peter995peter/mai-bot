import discord
from discord.commands import slash_command, OptionChoice
from discord.ext import commands
import songs
import random
import urllib
import math
import json
import page

def const_to_level(const):
    return f"{int(const)}{['', '+'][const%1 >= 0.55]}" #幫超過.6的定數補+

async def version_list(ctx: discord.AutocompleteContext): #版本號搜尋器
    rl = []
    versions = ["maimai", "maimai PLUS", "GreeN", "GreeN PLUS", "ORANGE", "ORANGE PLUS", "PiNK", "PiNK PLUS", "MURASAKi", "MURASAKi PLUS", "MiLK", "MiLK PLUS", "FiNALE", "DX", "DX PLUS", "Splash", "Splash PLUS", "UNiVERSE", "UNiVERSE PLUS", "FESTiVAL", "FESTiVAL PLUS", "BUDDiES", "BUDDiES PLUS", "PRiSM", "PRiSM PLUS","CiRCLE","CiRCLE PLUS"]
    version = ctx.value
    for i in versions:
        if version.lower() in i.lower():
            if len(rl) >= 25:
                break
            rl.append(OptionChoice(name=i, value=i))       
    return rl

def find_songs(mix_level=1.0, max_level=15.0, version=None, dx=-1, diff=None,region=None): #找出全部符合條件的鋪面
    if mix_level == None: #如果沒指定默認最小
        mix_level = 1.0
    if max_level == None: #如果沒有指定默認最大
        max_level = 15.0
    ok_data = []
    songss = songs.get() #抓取歌曲資料
    for song in songss:
        if ((version == None) or (songss[song]["version"] == version)): #檢查有沒有指定版本號
            for i in songss[song]["const"]:
                if dx == -1 or i.startswith(["STD_","DX_"][dx]): #檢查有沒有指定類別
                    if (songss[song]["const"][i] >= mix_level and songss[song]["const"][i] <= max_level) and (diff == None or i.endswith(diff)): #檢查定數是否在範圍還有不符不符合指定難度
                        if region == None or songss[song]["region"].get(region): #檢查那區域有沒有這首
                            ok_data.append({"name": song, "diff": i}) #都沒問題就存入資料
    return ok_data #輸出符合條件的資料

def song_embed(name, diff=None): #創建embed
    aka = {"False Amber (from the Black Bazaar, Or by A Kervan Trader from the Lands Afar, Or Buried Beneath ...":"False Amber (from the Black Bazaar, Or by A Kervan Trader from the Lands Afar, Or Buried Beneath the Shifting Sands That Lead Everywhere but Nowhere)"}
    if name in aka:
        name = aka.get(name)
    songss = songs.get() #取得歌曲資料
    embed = discord.Embed(title=f"{name}", description=f"更新版本：{songss[name]['version']}\n分類：{songss[name]['genre']}\n區域：日版{['❌','✅'][songss[name]['region']['JP']]} 國際版{['❌','✅'][songss[name]['region']['INT']]} 中國版{['❌','✅'][songss[name]['region']['CN']]}", colour=0x00b0f4)
    embed.set_author(name=songss[name]["artist"])
    embed.set_thumbnail(url=f"https://otoge-db.net/maimai/jacket/{songss[name].get('img','404.png')}")
    if diff == None:
        for i in songss[name]["const"]:
            query = urllib.parse.quote_plus(f'maimai {name} {i}') #讓使用者可以直接點擊搜尋
            embed.add_field(name=lte(i), value=f"難度: {const_to_level(songss[name]['const'][i])}({(songss[name]['const'][diff]) if (songss[name]['unknown'][diff] == 0) else ('~~' + str(songss[name]['const'][diff]) + '~~')})\n[在YouTube搜尋](https://www.youtube.com/results?search_query={query})", inline=False)
    else:
        if songss[name]['const'].get(diff,None) == None:
            diff = "DX_MASTER"
            if songss[name]['const'].get(diff,None) == None:
                diff = "STD_MASTER"
        query = urllib.parse.quote_plus(f'maimai {name} {diff}') #讓使用者可以直接點擊搜尋
        embed.add_field(name=lte(diff), value=f"難度: {const_to_level(songss[name]['const'][diff])}({(songss[name]['const'][diff]) if (songss[name]['unknown'][diff] == 0) else ('~~' + str(songss[name]['const'][diff]) + '~~')}))\n[在YouTube搜尋](https://www.youtube.com/results?search_query={query})", inline=False)
    return embed

def lte(text): #轉換文字成表情符號
    rep = {"STD_": "<:std1:1391324347670466602><:std2:1391324443405717604><:std3:1391324500582469733><:std4:1391324523160276993> ","DX_": "<:dx1:1391324687472267284><:dx2:1391324723547209769><:dx3:1391324751187677224><:dx4:1391324771077066843> "}
    for i in rep:
        text = text.replace(i,rep[i])
    return text

class List(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180,disable_on_timeout=True)
    @discord.ui.button(label="上一頁", style=discord.ButtonStyle.primary, emoji="⬅️")
    async def up(self, button, interaction):
        data = page.get()
        td = data.get(str(interaction.message.id), 404)
        if td == 404:
            await interaction.response.send_message("未找到資料，請嘗試重新輸入")
        elif td["page"] == 1:
            await interaction.response.send_message("你按了上一頁，但這已經是第一頁了")
        else:
            td["page"] -= 1
            songss = find_songs(td['mix_level'], td['max_level'], td['version'], td['dx'], td['diff'],td['region'])
            ss = []
            for s in songss[(td["page"]-1)*10:(td["page"])*10]:
                ss.append(song_embed(s.get("name"),s.get("diff")))
            await interaction.response.edit_message(content=f"page {td['page']}/{math.ceil(len(songss)/10)}",embeds=ss, view=List())
            data[str(interaction.message.id)] = td
            page.write(data)
    @discord.ui.button(label="下一頁", style=discord.ButtonStyle.primary, emoji="➡️")
    async def down(self, button, interaction):
        data = page.get()
        td = data.get(str(interaction.message.id), 404)
        if td == 404:
            await interaction.response.send_message("未找到資料，請嘗試重新輸入")
        elif td["page"] == td["max"]:
            await interaction.response.send_message("你按了下一頁，但這已經是最後一頁了")
        else:
            td["page"] += 1
            songss = find_songs(td['mix_level'], td['max_level'], td['version'], td['dx'], td['diff'],td['region'])
            ss = []
            for s in songss[(td["page"]-1)*10:(td["page"])*10]:
                ss.append(song_embed(s.get("name"),s.get("diff")))
            await interaction.response.edit_message(content=f"page {td['page']}/{math.ceil(len(songss)/10)}",embeds=ss, view=List())
            data[str(interaction.message.id)] = td
            page.write(data)

class song(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
    
    song = discord.SlashCommandGroup("song", "歌曲相關")

    @song.command(name='random',description='根據條件隨機抽歌')
    async def random1(self,ctx: discord.ApplicationContext,
    mix_level: discord.Option(float,name="最低等級",description="最低等級",required=False),
    max_level: discord.Option(float,name="最高等級",description="最高等級",required=False),
    version: discord.Option(str,autocomplete=version_list,required=False,name="指定版本",description="指定版本"),
    tp: discord.Option(str,choices=["DX","STD"],required=False,name="指定類型",description="指定類型"),
    diff: discord.Option(str,choices=["BASIC","ADVANCED","EXPERT","MASTER","Re:MASTER"],required=False,name="指定難度",description="指定難度"),
    region: discord.Option(str,choices=[OptionChoice(name="日版", value="JP"),OptionChoice(name="國際版", value="INT"),OptionChoice(name="中國版(舞萌DX)", value="CN")],required=False,name="指定區域",description="指定區域(國際版可能會缺部分歌曲)"),
    num: discord.Option(int,required=False,name="數量", description="要選幾首歌(可能會重複)",min_value=1, max_value=10)
    ):
        dx = {"STD": 0,"DX":1}.get(tp, -1)
        songss = find_songs(mix_level, max_level, version, dx, diff,region)
        if num == None:
            num = 1
        if len(songss) == 0: #完全沒找到的話
            await ctx.respond("未找到符合條件的鋪面")
        else:
            ss = []
            while len(ss) < num: #抽取直到達到數量
                s = random.choice(songss)
                ss.append(song_embed(s.get("name"),s.get("diff")))
            await ctx.respond(content=f"共{len(songss)}首符合條件",embeds=ss)
    
    @song.command(name='list',description='根據條件列出全部符合的歌曲')
    async def list(self,ctx: discord.ApplicationContext,
    mix_level: discord.Option(float,name="最低等級",description="最低等級",required=False),
    max_level: discord.Option(float,name="最高等級",description="最高等級",required=False),
    version: discord.Option(str,autocomplete=version_list,required=False,name="指定版本",description="指定版本"),
    tp: discord.Option(str,choices=["DX","STD"],required=False,name="指定類型",description="指定類型"),
    diff: discord.Option(str,choices=["BASIC","ADVANCED","EXPERT","MASTER","Re:MASTER"],required=False,name="指定難度",description="指定難度"),
    region: discord.Option(str,choices=[OptionChoice(name="日版", value="JP"),OptionChoice(name="國際版", value="INT"),OptionChoice(name="中國版(舞萌DX)", value="CN")],required=False,name="指定區域",description="指定區域(國際版可能會缺部分歌曲)")
    ):
        dx = {"STD": 0,"DX":1}.get(tp, -1)
        songss = find_songs(mix_level, max_level, version, dx, diff,region)
        ss = []
        for s in songss[0:10]:
            ss.append(song_embed(s.get("name"),s.get("diff")))
        em = await ctx.respond(f"page 1/{math.ceil(len(songss)/10)}",embeds=ss, view=List())
        em = await em.original_response()
        data = page.get()
        data[str(em.id)] = {
        "author": ctx.author.id,
        "mix_level": mix_level,
        "max_level": max_level,
        "version": version,
        "dx": dx,
        "diff": diff,
        "region": region,
        "page": 1,
        "max": math.ceil(len(songss)/10)
        }
        page.write(data)
    
    @song.command(name='find',description='尋找指定歌曲')
    async def ping(self,ctx: discord.ApplicationContext):
        await ctx.respond(f"等等寫")
    
    @song.command(name='update',description='幫我更新一下歌曲資料庫')
    async def ping(self,ctx: discord.ApplicationContext):
        em = await ctx.respond(f"開始更新")
        sgs = songs.update()
        await em.edit(content=f"更新完成 當前歌曲數量{len(sgs)}")

def setup(bot):
    bot.add_cog(song(bot))