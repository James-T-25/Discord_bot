import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

class MyClient(discord.Client):
    def __init__(self, *, intents, **options) -> None:
        super().__init__(intents=intents, **options)
        self.tree = discord.app_commands.CommandTree(self)

    async def on_ready(self):
        await self.tree.sync(guild=discord.Object(id=790714282551017512))
        print('Logged on as', self.user)

intents = discord.Intents.default()
intents.message_content = True
myclient = MyClient(intents=intents)

@myclient.tree.command(name="ping", guild = discord.Object(id= 790714282551017512))
async def ping(interaction:discord.Interaction):
    await interaction.response.send_message("Pong!", ephemeral=True)

myclient.run(os.getenv('bot_token'))