import discord
from discord.commands import slash_command, OptionChoice
from discord.ext import commands
import json

with open("help.json") as file:
    data = json.load(file)

cat_list = []
cat_opt = []
cmd_list = []
cmd_opt = []
cmd_cat = {}
for i in data:
    cat_list.append(OptionChoice(name=data[i]["name"], value=i))
    cat_opt.append(discord.SelectOption(label=data[i]["name"],description=data[i]["name"],value=i))
    for i2 in data[i]["commands"]:
        cmd_list.append(i2)
        cmd_opt.append(discord.SelectOption(label=i2,description=data[i]["commands"][i2]["content"][0],value=i2))
        cmd_cat[i2] = i

class MyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
    @discord.ui.select(
        placeholder = "選擇一個類別",
        min_values = 1,
        max_values = 1,
        options = cat_opt
    )
    async def cat_sel(self, select, interaction):
        cat = select.values[0]
        embed = discord.Embed(title=data[cat]["name"], colour=0x00b0f4)
        for i in data[cat]["commands"]:
            embed.add_field(name=f'`{i}`',value="\n".join(data[cat]["commands"][i]["content"][:2]),inline=False)
        await interaction.response.edit_message(embed=embed,view=self)
    @discord.ui.select(
        placeholder = "選擇一個指令",
        min_values = 1,
        max_values = 1,
        options = cmd_opt
    )
    async def cmd_sel(self, select, interaction):
        cmd = select.values[0]
        cat = cmd_cat[cmd]
        embed = discord.Embed(title=cmd, description="\n".join(data[cat]["commands"][cmd]["content"]) ,colour=0x00b0f4)
        embed.set_image(url=data[cat]["commands"][cmd]["img"])
        await interaction.response.edit_message(embed=embed,view=self)

class help(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @slash_command(name='help',description='查看機器人指令幫助')
    async def help(self,ctx: discord.ApplicationContext,
    cat: discord.Option(str,choices=cat_list,required=False,name="指定類別",description="與指定指令2選1(也可以都不選)"),
    cmd: discord.Option(str,choices=cmd_list,required=False,name="指定指令",description="與指定類別2選1(也可以都不選)"),
    ):
        if cat != None:
            embed = discord.Embed(title=data[cat]["name"], colour=0x00b0f4)
            for i in data[cat]["commands"]:
                embed.add_field(name=f'`{i}`',value="\n".join(data[cat]["commands"][i]["content"][:2]),inline=False)
        elif cmd != None:
            cat = cmd_cat[cmd]
            embed = discord.Embed(title=cmd, description="\n".join(data[cat]["commands"][cmd]["content"]) ,colour=0x00b0f4)
            embed.set_image(url=data[cat]["commands"][cmd]["img"])
        else:
            embed = discord.Embed(title="指令幫助", colour=0x00b0f4)
            for i in data:
                embed.add_field(name=data[i]["name"],value=(' | '.join(list(data[i]['commands']))))
        await ctx.respond(embed=embed,view=MyView())

def setup(bot):
    bot.add_cog(help(bot))