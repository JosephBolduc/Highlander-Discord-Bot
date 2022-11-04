#Credit to realpython

import discord
from discord.ext import commands
from pathlib import Path
import json
from Player import Player

TF2CLASSES = ["scout", "soldier", "pyro", "demo", "heavy", "engineer", "medic", "sniper", "spy"]
LEAGUES = ["rgl", "ugc"]
ROLES = ["main caller", "Starter", "Alternate", "mentor"]

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

tokenFile = json.load(open(cwd+"/credentials.json"))

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='tf_', intents = intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

    status = discord.Status.do_not_disturb
    game = discord.Game("Microsoft Visual Studio")
    await bot.change_presence(status=status, activity=game)

@bot.event
async def on_member_join(member):
    #await member.create_dm()
    #await member.dm_channel.send("Welcome to the SB Highlander Server")
    pass

@bot.command(name="addSelfToJSON")
async def addSelfToJSON(ctx):
    name = str(ctx.author)
    displayname = ctx.author.display_name
    roles = ctx.author.roles

    response = f"{name}, {displayname}, "
    for item in roles:
        if item.name != "@everyone":
            response += item.name + " "

    print(response)
    await ctx.send(response)

    userObject = Player(name, [displayname], [], [], [])

    print("\nadded roles:")
    print(userObject.name)
    print(userObject.aliases)
    print(userObject.leagues)
    print(userObject.classes)
    print(userObject.roles)

@bot.command(name="addUserToJSON")
async def addUserToJSON(ctx, user: str):
    name = discord.utils.get(ctx.guild.members, name=user)
    displayname = name.display_name
    roles = name.roles

    response = f"{name}, {displayname}, "
    for item in roles:
        if item.name != "@everyone":
            response += item.name + " "

    print(response)
    await ctx.send(response)

    userObject = Player(name, [displayname], [], [], [])

    print("\nadded roles:")
    print(userObject.name)
    print(userObject.aliases)
    print(userObject.leagues)
    print(userObject.classes)
    print(userObject.roles)

@bot.command(name='get_status', help='returns the status of the bot')
async def getStatus(ctx):
    await ctx.send("I'm doing fine")

@bot.command(name='create_channel')
@commands.has_role('sex')
async def create_channel(ctx, channel_name='deep blue jeer zone'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)

@bot.command(name="say")
@commands.has_role('sex')
async def say(ctx, message: str):
    guild = ctx.guild
    general = discord.utils.get(guild.channels, name="general")
    await general.send(message)

@bot.command(name="encourage")
async def encourage(ctx, user: str):
    result = "you should kill yourself " + user
    guild = ctx.guild
    general = discord.utils.get(guild.channels, name="general")
    await general.send(result)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(tokenFile["token"])