import discord
from discord.ext import commands, tasks
import asyncio
from stuff.CustomExceptions import ArgumentError

class ErrorHandling(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exception):
        print(type(exception))
        if isinstance(exception, ArgumentError):
            await ctx.send(exception.message)
        
        elif isinstance(exception, commands.MissingRequiredArgument):
            await ctx.send("You are `missing at least 1 argument` to sufficiently run this command")
        
        elif isinstance(exception, commands.CommandOnCooldown):
            await ctx.send("Command on cooldown, try again in `{:.2f}` seconds".format(exception.retry_after))

def setup(client):
    client.add_cog(ErrorHandling(client))