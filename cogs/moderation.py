import discord
import random
from discord.ext import commands, tasks
from itertools import cycle
from Main import get_world

class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Game(name = "Nah I'm actually not|Use k.help to see what I can do 👀"))

    @commands.command(help = "Use the command like: ```k.clear <number>``` This deletes a specified number of messages in the channel")
    @commands.has_permissions(manage_messages = True)
    async def clear(self,ctx, amount = 1):
        message = str(amount)+" messages were deleted."
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(message) 

    @commands.command(help = "Use the command like: ```k.blacklist <words separated by commas>``` This adds to the list of words not allowed in the server")
    @commands.has_permissions(manage_messages = True)
    async def blacklist(self, ctx, *,message):
        call_location = get_world().get_guild(ctx.guild.id)
        successfully_added = []
        words = message.split(", ")

        for word in words:
            if call_location.blacklist_word(word.lower()):
                successfully_added.append(word)

        print(call_location.blacklisted_words)
        if successfully_added:
            await ctx.channel.send("Successfully blacklisted "+", ".join(successfully_added))
        else:
            await ctx.channel.send(f"The word/s ```{message}``` have already been added.")

    @commands.command(help = "Use the command like: ```k.kick <member>``` Removes a user from the guild")
    @commands.has_permissions(kick_members = True)
    async def kick(self,ctx, member: discord.Member,*,reason = None):
        await member.kick(reason=reason)

    @commands.command(help = "Use the command like: ```k.profanityFilter <on/off>``` This dictates whether blacklisted words be allowed on the server")
    @commands.has_permissions(kick_members = True, manage_messages = True)
    async def profanityFilter(self,ctx,message):
        call_location = get_world().get_guild(ctx.guild.id)
        if message.lower() == 'on':
            call_location.set_psetting(True)

        elif message.lower()=='off':
            call_location.set_psetting(False)

        else:
            await ctx.channel.send('Invalid input. Expected argument: "on" or "off"')

    @commands.Cog.listener()
    async def on_message(self, message):
        call_location = get_world().get_guild(message.guild.id)
        word_list = call_location.blacklisted_words
        if not message.author.bot and not message.content.startswith("k.blacklist") and word_list and call_location.profanity_setting:
            for x in word_list:
                if x in message.content:
                    user =  message.author.id
                    await message.channel.purge(limit= 1)
                    await message.channel.send(f'<@{user}> Swore!')
                    break



def setup(client):
    client.add_cog(moderation(client))