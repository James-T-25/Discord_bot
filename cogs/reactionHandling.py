import discord
from discord.ext import commands, tasks
from stuff.player import Player
from Main import get_world

class reaction_handler(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user):
        if not user.bot:
            call_location = get_world().get_guild(reaction.message.guild.id)
            mssg_id = str(reaction.message.id)    
            l = get_world().get_lotteries().get(mssg_id)
            emoji = reaction.emoji
            call_location.add_user(user.id)
            call_location.add_user(reaction.message.author.id)

            if l and emoji == "✋":
                print("reaction received")
                get_world().get_lotteries().get(mssg_id)[0].append(user)

            
            elif emoji in ["👍","👎"]:
                player1 = call_location.get_playerobj(user.id)
                player2 = call_location.get_playerobj(reaction.message.author.id)
                if emoji == "👍" and  reaction.message.author.id != user.id:
                    player2.add_merit(4)
                    player1.add_merit(1)
                elif emoji == "👎" and  reaction.message.author.id != user.id:
                    player2.add_merit(-2)
                    player1.add_merit(1)

        
    @commands.Cog.listener()
    async def on_reaction_remove(self,reaction, user):
        if not user.bot:
            call_location = get_world().get_guild(reaction.message.guild.id)
            mssg_id = str(reaction.message.id)
            lottery= get_world().get_lotteries().get(mssg_id)
            emoji = reaction.emoji

            if lottery and emoji == "✋":
                lottery_entrants = lottery[0]
                print("reaction removed event processed")
                lottery_entrants.remove(user)

            elif emoji in ["👍","👎"]:
                player1 = call_location.get_playerobj(user.id)
                player2 = call_location.get_playerobj(reaction.message.author.id)
                if emoji == "👍" and  reaction.message.author.id != user.id:
                    player2.add_merit(-4)
                    player1.add_merit(-1)
                elif emoji == "👎" and  reaction.message.author.id != user.id:
                    player2.add_merit(2)
                    player1.add_merit(-1)

def setup(client):
    client.add_cog(reaction_handler(client))