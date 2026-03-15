import discord
from discord.commands import slash_command
from discord.ext import commands
from fun import songs,mainet,link
from cogs import song
import math

def ratingCal(lv,acc):
    if acc >= 100.5: #SSS+
        acc = 100.5
        mp = 0.224
    elif acc >= 100: #SSS
        mp = 0.216
    elif acc >= 99.5: #SS+
        mp = 0.211
    elif acc >= 99: #SS
        mp = 0.208
    elif acc >= 98: #S+
        mp = 0.203
    elif acc >= 97: #S
        mp = 0.2
    elif acc >= 94: #AAA
        mp = 0.168
    elif acc >= 90: #AA
        mp = 0.136
    elif acc >= 80: #A
        mp = 0.136
    else:
        mp = 0 #因為我不知道
    return math.floor(lv*acc*mp)

class game(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @slash_command(name='score',description='查詢自己指定歌曲的分數',integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
    async def score(self,ctx: discord.ApplicationContext,
    name: discord.Option(str,autocomplete=song.song_list,required=True,name="歌曲名稱",description="歌曲名稱"),
    diff: discord.Option(str,choices=["BASIC","ADVANCED","EXPERT","MASTER","Re:MASTER"],required=False,name="指定難度",description="指定難度(未指定則默認全部)")):
        Mid = link.DidToMid(ctx.author.id)
        if Mid is None:
            await ctx.respond("你尚未綁定帳號，請先使用/link綁定")
        else:
            em = await ctx.respond("讀取中")
            songss = songs.get().get(name,None)
            if songss is None:
                embed = discord.Embed(title=name, description="未找到這首歌的資料", colour=0x00b0f4)
            embed = discord.Embed(title=name, description=mainet.getInfo(Mid)["name"], colour=0x00b0f4)
            embed.set_author(name=songss["artist"])
            embed.set_thumbnail(url=f"https://otoge-db.net/maimai/jacket/{songss.get('img','404.png')}")
            if diff is None:
                diff = ["BASIC","ADVANCED","EXPERT","MASTER","Re:MASTER"]
            else:
                diff = [diff]
            for i in diff:
                await em.edit(content=f"正在讀取{i}")
                data = mainet.getScore(Mid,i).get(name,None)
                if data is not None:
                    for i2 in data:
                        diff2 = ('DX_' if i2['dx'] else 'STD_')+i
                        embed.add_field(name=song.lte(diff2), value=f"難度: {song.const_to_level(songss['const'][diff2])}({(songss['const'][diff2]) if (songss['unknown'][diff2] == 0) else ('~~' + str(songss['const'][diff2]) + '~~')})\n達成率: {i2['acc']}%\n單曲Rating: {ratingCal(songss['const'][diff2],i2['acc'])}", inline=False)
            await em.edit(content="",embed=embed)

    @slash_command(name='info',description='查詢指定玩家綁定的個人資訊',integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
    async def info(self,ctx: discord.ApplicationContext,
    user: discord.Option(discord.SlashCommandOptionType.user,required=False,name="指定玩家",description="要查看的人")):
        em = await ctx.respond("讀取中")
        if user is None:
            user = ctx.author
        Mid = link.DidToMid(user.id)
        if Mid is None:
            await em.edit(content="他還沒有綁定帳號，請先讓他使用/link綁定後再試")
        else:
            data = mainet.getInfo(Mid)
            print(data)
            embed = discord.Embed(title=data["name"], description=f"Rating: {data['rating']}")
            embed.set_thumbnail(url=data['icon']) #不知道為什麼抓不到，已放棄
        await em.edit(content="",embed=embed)
def setup(bot):
    bot.add_cog(game(bot))