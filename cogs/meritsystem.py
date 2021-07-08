import discord
from discord.ext import commands, tasks
from Main import get_world
from stuff.Converters import custom_emoji_converter

class meritsystem(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help = "Use the command like: ```k.profile <member>``` This brings up the profile of the mentioned")
    async def profile(self, ctx, member:discord.Member = None):
        if member == None:
            cmd = self.client.get_command("help")
            await cmd.__call__(ctx, "profile")
            return

        call_location = get_world().get_guild(ctx.guild.id)
        membr = call_location.get_playerobj(member.id)
        created = member.created_at.date()
        joined = member.joined_at.date()
        av_url = member.avatar_url

        desc = f"ℂ𝕒𝕞𝕖 𝕚𝕟𝕥𝕠 𝕖𝕩𝕚𝕤𝕥𝕖𝕟𝕔𝕖 𝕠𝕟: ```{created}```  \n𝕁𝕠𝕚𝕟𝕖𝕕 𝕥𝕙𝕚𝕤 𝕤𝕖𝕣𝕧𝕖𝕣 𝕠𝕟: ```{joined}```"
        awrd_str_rep = "None"
        row = []

        if membr:
            awards = membr.get_awards()
            if len(awards.keys()) != 0:
                awrd_str_rep = ""

            for key in awards:
                list1 = awards[key]
                visual = list1[0]

                if type(list1[0]) == int:
                    visual = self.client.get_emoji(list1[0])

                sect = f"{key} {visual} x {list1[1]}"
                row.append(sect)
                if len(row) == 5:
                    awrd_str_rep += "\t".join(row) + "\n"
                    row = []
            awrd_str_rep += "\t".join(row) + "\n"    

            embed = discord.Embed(title = "Profile", description = desc ,colour = member.colour)
            embed.set_author(name = member.display_name, icon_url=av_url)
            embed.add_field(name = "<a:star_spin:859556349524443136> 𝕊𝕖𝕣𝕧𝕖𝕣 𝕄𝕖𝕣𝕚𝕥: ", value = str(membr.get_server_merit()))
            embed.add_field(name = "Awards", value = awrd_str_rep, inline=False)
            await ctx.send(embed= embed)

        else:
            call_location.add_user(member.id)
            await self.client.process_commands(ctx.message)

    @commands.command()
    async def awards(self, ctx):
        call_location = get_world().get_guild(ctx.guild.id)
        available_awards  = call_location.get_awards()
        names = ""
        awards = ""
        cost = ""


        for key in available_awards.keys():
            val = available_awards[key]
            if type(val[0]) == int:
                emoji = self.client.get_emoji(val[0])
                awards += str(emoji) + "\n"
            else:
                awards += val[0] + "\n"
            
            names += key + "\n"
            cost += str(val[1]) + "\n"


        desc = "These are the awards available on this server to be purchased with your accumulated Server Merit."
        embed = discord.Embed(title = "🏆 Awards", description = desc)
        embed.add_field(name = "Name", value=names)
        embed.add_field(name = "Awards", value= awards)
        embed.add_field(name = "Merit cost", value = cost)

        await ctx.send(embed = embed)
    
    @commands.command()
    async def add_award(self, ctx, name, emoji:custom_emoji_converter, price :int):
        call_location = get_world().get_guild(ctx.guild.id)
        
        if type(emoji) != str:
            call_location.add_award(name, emoji.id, price)
        else:

            call_location.add_award(name, emoji, price)

        await ctx.send(f"Successfully added the {name} award {emoji} with the price {price}")

    @commands.command()
    async def get_award(self, ctx, *,message):
        args = message.split(",")
        call_location = get_world().get_guild(ctx.guild.id)
        user = call_location.get_playerobj(ctx.author.id)
        available_awards = call_location.get_awards()
        award = available_awards.get(args[0])

        user.add_merit(award[1]*-1)

        if award == "None":
            await ctx.send(f"The requested `{args[0]}` award does not exist")
            return
        
        else:
            user.add_award(args[0], award[0])
            await ctx.send(f"You have acquired the requested `{args[0]}` award; see your profile for confirmation")



def setup(client):
    client.add_cog(meritsystem(client))