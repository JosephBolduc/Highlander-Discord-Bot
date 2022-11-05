#Credit to realpython for starting out the bot
import discord
from discord.ext import commands

from pathlib import Path
import json

import shelve # Database, what for?

from Player import Player


# Initializing random stuff
TF2CLASSES = ["Scout", "Soldier", "Pyro", "Demoman", "Heavy", "Engineer", "Medic", "Sniper", "Spy"]
LEAGUES = ["RGL", "UGC"]
ROLES = ["main caller", "Starter", "Alternate", "Mentor"]
serverUserObjects = [] # Stores the players on the server
openSecretChannels = [] # Opened secret channels


# Gets discord and firebase credentials
cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")
tokenFile = json.load(open(cwd+"/credentials.json"))


# Sets up bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='tf_', intents = intents)



# Bot Events

@bot.event
async def on_ready():
    await trimOldChannels()
    status = discord.Status.do_not_disturb
    game = discord.CustomActivity("Currently under construction...")
    await bot.change_presence(status=status, activity=game)
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_member_join(member):
    #await member.create_dm()
    #await member.dm_channel.send("Welcome to the SB Highlander Server")
    pass

'''
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
'''


# Bot Commands 

@bot.command(name="test_db")
async def testDB(ctx, DBname):
    createDB(DBname)


@bot.command(name="addSelfToJSON")
async def addSelfToJSON(ctx):
    name = str(ctx.author)
    aliases = [ctx.author.display_name]
    roles = []

    for item in ctx.author.roles:
        if item.name != "@everyone":
            roles.append(str(item.name))

    userObject = createUserObject(name, aliases, roles) # Function does the role sorting
   
    await ctx.send("Player object:\n" + userObject.__str__())
    await ctx.send("Database entry:\n" + userObject.jsonify())


@bot.command(name="addAllToJSON")
async def addAllToJSON(ctx):
    serverMembers = ctx.guild.members
    for member in serverMembers:
        if member != bot.user:
            name = str(member)
            aliases = [member.display_name]
            roles = []

            for item in member.roles:
                if item.name != "@everyone":
                    roles.append(str(item.name))
            serverUserObjects.append(createUserObject(name, aliases, roles)) # Function does the role sorting

    await ctx.send("Finished processing server users...\nDB entries:")
    
    for item in serverUserObjects:
        await ctx.send(str(item.jsonify()))
    

@bot.command(name='get_status', help='returns the status of the bot')
async def getStatus(ctx):
    await ctx.send("I'm doing fine")


@bot.command(name='create_channel')
@commands.has_role('sex')
async def create_channel(ctx, channel_name):
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
    result = "you should love yourself " + user + "!"
    guild = ctx.guild
    general = discord.utils.get(guild.channels, name="general")
    await general.send(result)


@bot.command(name="create_rsvp")
async def createRSVP(ctx, username):
    user = discord.utils.get(ctx.guild.members, name=username)
    await rsvpForMatch(ctx, user)



# Helper Functions

def createUserObject(name, aliases, roles):
    roles.reverse()
    userObject = Player(name, roles, aliases)
    return userObject


async def rsvpForMatch(ctx, user):
    takenChannels = len(openSecretChannels)
    newChannelName = "Match-RSVP-" + str(takenChannels+1)
    openSecretChannels.append(newChannelName)

    channel = await ctx.guild.create_text_channel(newChannelName)

    print(user)
    #sets perms
    everyone = ctx.guild.roles[0]
    await channel.set_permissions(everyone, view_channel=False)
    await channel.set_permissions(user, view_channel=True)


async def trimOldChannels():
    for server in bot.guilds:
        for channel in server.channels:
            if len(channel.name) >= 11:
                if channel.name[0:10] == "match-rsvp":
                    print("Trimmed", channel, "from", channel.guild)
                    await channel.delete(reason="leftover channel")
    print("Finished trimming")



# Shelve DB Functions

def createDB(name):
    with shelve.open("shelves\\"+name) as db:
        db["players"] = {}
        db["events"] = {}

# Runner
bot.run(tokenFile["token"])