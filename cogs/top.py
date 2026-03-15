import discord
from discord.commands import slash_command, OptionChoice
from discord.ext import commands
from fun import link, mainet,songs
from cogs import song

class top(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
    
    top = discord.SlashCommandGroup("top", "排行榜相關",integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})

    @top.command(name='rating',description='查看Rating排行榜')
    async def rating(self,ctx: discord.ApplicationContext,
    region: discord.Option(str,choices=[OptionChoice(name="全球", value="All"),OptionChoice(name="機器人", value="BOT")],required=True,name="排行區域",description="排行區域"),
    num: discord.Option(int,required=False,name="數量", description="要顯示多少名(預設10名)",min_value=1,max_value=100)
    ):
        em = await ctx.respond("讀取中")
        if num is None:
            num = 10
        sd,st=[],""
        if region == "BOT":
            data = link.Get()
            for i in data:
                sd.append({"user": i,"rating": mainet.getInfo(data[i])["rating"]})
            sd = sorted(sd, key=lambda x: x["rating"], reverse=True)[:num]
            n = 1
            yr = -1
            for i in sd:
                if i['user'] == str(ctx.author.id):
                    yr = n
                st += f"{n}. <@{i['user']}>: {i['rating']}\n"
                n += 1
            embed = discord.Embed(title=f"Rating排行榜(機器人)", description=st, colour=0x00b0f4)
            if yr != -1:
                embed.set_footer(text=f"你在第{yr}名")
            else:
                embed.set_footer(text="你未上榜")
            await em.edit(content="",embed=embed)
        else:
            soup = mainet.get("ranking/deluxeRating/")
            names = soup.select("div.f_l.p_t_10.p_l_10.f_15")
            ratings = soup.select("div.rating_block")
            n = 0
            while n < min(num,len(names)):
                n += 1
                st += f"{n}. {names[n-1].text.strip()}: {ratings[n].text.strip()}\n"
            embed = discord.Embed(title=f"Rating排行榜(全球)", description=st[:4000], colour=0x00b0f4)
            await em.edit(content="",embed=embed)
    
    @top.command(name='score',description='查看歌曲排行榜')
    async def score(self,ctx: discord.ApplicationContext,
    name: discord.Option(str,autocomplete=song.song_list,required=True,name="歌曲名稱",description="歌曲名稱"),
    diff: discord.Option(str,choices=["BASIC","ADVANCED","EXPERT","MASTER","Re:MASTER"],required=True,name="指定難度",description="指定難度(未指定則默認全部)"),
    tp: discord.Option(str,choices=["DX","STD"],required=True,name="指定類型",description="指定類型"),
    region: discord.Option(str,choices=[OptionChoice(name="全球", value="All"),OptionChoice(name="機器人", value="BOT")],required=True,name="排行區域",description="排行區域"),
    num: discord.Option(int,required=False,name="數量", description="要顯示多少名(預設10名)",min_value=1,max_value=100)
    ):
        em = await ctx.respond("讀取中")
        if num is None:
            num = 10
        sd,st=[],""
        songss = songs.get().get(name,None)
        if songss is None:
            await em.edit(content="未找到這首歌的資料")
        elif f"{tp}_{diff}" not in songss["const"]:
            await em.edit(content="未找到這首歌的難度")
        elif region == "BOT":
            data = link.Get()
            for i in data:
                sc = mainet.getScore(data[i], diff).get(name,[])
                for i2 in sc:
                    if i2["dx"] == {"STD": False,"DX": True}[tp]:
                        sd.append({"user": i,"acc":i2["acc"]})
            sd = sorted(sd, key=lambda x: x["acc"], reverse=True)[:num]
            n = 1
            yr = -1
            for i in sd:
                if i['user'] == str(ctx.author.id):
                    yr = n
                st += f"{n}. <@{i['user']}>: {i['acc']}%\n"
                n += 1
            embed = discord.Embed(title="成績排行榜(機器人)", description=f"{name}\n{song.lte(f'{tp}_{diff}')}\n難度: {song.const_to_level(songss['const'][f'{tp}_{diff}'])}({(songss['const'][f'{tp}_{diff}']) if (songss['unknown'][f'{tp}_{diff}'] == 0) else ('~~' + str(songss['const'][f'{tp}_{diff}']) + '~~')})\n\n{st}", colour=0x00b0f4)
            embed.set_author(name=songss["artist"])
            embed.set_thumbnail(url=f"https://otoge-db.net/maimai/jacket/{songss.get('img','404.png')}")
            if yr != -1:
                embed.set_footer(text=f"你在第{yr}名")
            else:
                embed.set_footer(text="你未上榜")
            await em.edit(content="",embed=embed)
        else:
            await em.edit(content="還沒寫")

def setup(bot):
    bot.add_cog(top(bot))