import discord
import asyncio
from discord.ext import commands
from Main import get_client
from stuff.CustomExceptions import ArgumentError


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

class dur_secs_converter(commands.Converter):
    async def convert (self, ctx, argument:str):
        time = argument.split(":")
        dur_secs = 0
        
        if not len(time) == 4 or not argument.replace(":","").isdigit():
            dur_secs = None
            raise ArgumentError("Incorrect input and/or format for the duration field")

        else:
            dur_secs += int(time[0]) * 86400 + int(time[1]) * 3600 + int(time[2]) * 60 + int(time[3])
        
        return dur_secs

