import discord
from discord.commands import slash_command
from discord.ext import commands
from fun import mainet, link

class link2(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @slash_command(name='link',description='綁定帳號',integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
    async def link(self,ctx: discord.ApplicationContext,
    code: discord.Option(int,name="好友代碼",description="前往maimai DX NET獲取",required=True)
    ):
        data = link.Get()
        if str(ctx.author.id) in data:
            await ctx.respond("你已經綁定了一個帳號，如果需要換綁請先/unlink")
        elif code in data.values():
            await ctx.respond("這帳號已經被別人綁定了")
        else:
            em = await ctx.respond("讀取中")
            info = mainet.getInfo(code)
            if info is None:
                em = await em.edit(content="你好像還沒加入機器人好友，正在嘗試加入")
                if mainet.addFriend(code):
                    await em.edit(content="你好像還沒加入機器人好友，正在嘗試加入\n應該成功了，請打開maimai DX NET查看，完成後再次輸入")
                else:
                    await em.edit(content="你好像還沒加入機器人好友，正在嘗試加入\n發生未知錯誤，請稍後重試")
            else:
                data[str(ctx.author.id)] = code
                link.Write(data)
                await em.edit(content=f"綁定成功{info['name']}")


    @slash_command(name='unlink',description='解除綁定帳號',integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
    async def unlink(self,ctx: discord.ApplicationContext):
        data = link.Get()
        if data.get(str(ctx.author.id), None) is not None:
            del data[str(ctx.author.id)]
            link.Write(data)
            await ctx.respond("成功解綁")
        else:
            await ctx.respond("你還沒有綁定，不能解綁")

def setup(bot):
    bot.add_cog(link2(bot))