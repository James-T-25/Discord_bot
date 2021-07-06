import discord
import asyncio
from discord.ext import commands
from Main import get_client

class custom_emoji_converter(commands.Converter):
    async def convert(self, ctx, argument):
        emoji = None
        if type(argument) == discord.Emoji:
            emoji = argument
        elif type(argument) == str:
            if argument.isdigit():
                client = get_client()
                emoji = client.get_emoji(int(argument))

            else:
                emoji = argument

        return emoji
        