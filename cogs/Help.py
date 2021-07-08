import discord
from discord.ext import commands, tasks

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.command_dict = {}

    @commands.Cog.listener()
    async def on_ready(self):
        for cog_name in self.client.cogs:
            command_list = self.client.cogs[cog_name].get_commands()
            for cmd in command_list:
                self.command_dict[cmd.name] = cmd


    @commands.command()
    @commands.bot_has_permissions(embed_links = True)
    async def help(self, ctx, message:str = None):
        if message:
            embed = discord.Embed(title = f"Command Info: {message}", description = self.command_dict[message].help, colour = discord.Color.red() )         
            print(self.command_dict[message].help)
        else:
            embed = discord.Embed(title = "Help", description = "k.help <command name> to obtain further information about a command available",
            colour = discord.Color.red())
          
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.add_field(name = "Moderation",value = "```blacklist, clear, kick, profanityFilter```")
            embed.add_field(name = "Other", value= "```define, lottery, end_lottery, profile```", inline= False)
        
        await ctx.send(embed = embed)



def setup(client):
    client.add_cog(Help(client))