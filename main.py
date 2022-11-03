#Credit to realpython

import discord
from discord.ext import commands
from pathlib import Path
import json

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

tokenFile = json.load(open(cwd+"/credentials.json"))

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='tf_', intents = intents)

@bot.event
async def on_ready():
    status = discord.Status.do_not_disturb
    activity = discord.CustomActivity(name="Currently under construction...", emoji=":construction:")
    await bot.change_presence(status=status, activity=activity)

    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_member_join(member):
    #await member.create_dm()
    #await member.dm_channel.send("Welcome to the SB Highlander Server")
    pass



@bot.command(name='get_status', help='returns the status of the bot')
async def getStatus(ctx):
    await ctx.send("I'm doing pretty ok")

@bot.command(name="pick_random_class")
async def pickClass(ctx, value: int):
    tf2Classes = ["scout", "soldier", "pyro", "demo", "heavy", "engie", "med", "sniper", "spy"]
    response = "You should play ", tf2Classes[value]
    await ctx.send(response)

@bot.command(name='create_channel')
@commands.has_role('me lol')
async def create_channel(ctx, channel_name='deep blue jeer zone'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')



bot.run(tokenFile["token"])