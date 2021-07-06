import os
import discord
from discord.ext import commands
from stuff.botdomain import World
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents().default()
intents.members = True

client = commands.AutoShardedBot(
    command_prefix= ["k."],
    case_insensitive = True,
    intents = intents
)

client.remove_command("help")

world = World()

def get_world() -> World:
    return world

def get_client() -> discord.Client:
    return client

@client.event
async def on_ready():
    for home in client.guilds:
        world.add_guild(home.id)
    print('Bot is ready.')

@client.command(hidden = True)
@commands.is_owner()
async def load(ctx, extension):
    try:
        client.load_extension(f'cogs.{extension}')
        print(f'{extension} has been loaded')
    except Exception as err:
        print(err)
        raise err

@client.command(hidden = True)
@commands.is_owner()
async def unload(ctx, extension):
    try:
        client.unload_extension(f'cogs.{extension}')
        print(f'{extension} has been unloaded')
    except Exception as err:
        print(err)
        raise err

@client.command(hidden=True)
@commands.is_owner()
async def reload(ctx, extension):
    try: 
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        print(f'{extension} has been reloaded')

    except Exception as err:
        print(err)
        raise err

@client.command(hidden=True)
@commands.is_owner()
async def end(ctx):
    embed = discord.Embed(title = "Farewell", colour = discord.Colour.red())
    embed.set_image(url= "https://media.giphy.com/media/sJ7EDbXwEIygU/giphy.gif")
    await ctx.send(embed = embed)
    await ctx.bot.logout()


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency*1000)} ms')


client.run(os.getenv("token"))