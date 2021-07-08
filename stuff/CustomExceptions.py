import discord
from discord.ext import commands
class ArgumentError(commands.MissingRequiredArgument):
    def __init__(self, message):
        self.message = message