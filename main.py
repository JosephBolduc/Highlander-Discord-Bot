# Credit to realpython for starting out the bot

# discord.py
import discord
from discord.ext import commands

# reading credentials.json
from pathlib import Path
import json

# "database" and structure
from ShelveDB import *        # Database, what for?
from Player import Player     # Database architecture, what for?
from Event import Event

# random functions/cogs
from HelperFunctions import *
from ChatReactions import ChatReactions

# event loop code
from EventThread import EventThread


eventThread = None
eventList = {}			# joseph 2nd worst piece of code 2022 award goes here
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
	setupTimeThread()
	await bot.add_cog(ChatReactions(bot))
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

# Command implicitly takes the args of the event name, role to add to roster, and the date
@bot.command("create_event", help="Creates an event, takes arguments in the form \"Event name @roleToAddToRoster HH:MM DD/MM/YYYY\" ")
async def create_event(ctx):
	inputString = str(ctx.message.content)
	inputString = inputString[16:]

	eventName = ""
	roleID = ""
	dateString = ""
	stringBuilder = ""

	# Searches input string for @everyone to add everyone to the server
	if inputString.find("@everyone") > -1:
		await ctx.send("Found @everyone, will implement later...")
		return None

	for index in range(0, len(inputString)):
		currentChar = inputString[index]

		# Finds the start of the discord role id and flushes stringBuilder to eventName
		if currentChar == "<":
			if inputString[index+1] == "@":
				eventName = stringBuilder[0:-1]
				stringBuilder = ""
		
		# Finds the end of the discord role id and flushes stringBuilder to roleID
		if currentChar == ">":
			roleID = stringBuilder[3:]
			stringBuilder = ""

		# Empties the last of stringBuilder, which should only be the date, into datestring
		stringBuilder += currentChar
	dateString = stringBuilder[2:]

	roster = []

	for user in ctx.guild.members:
		for userRole in user.roles:
			if int(userRole.id) == int(roleID):
				roster.append(user.id)

	activeDB = pullDB(ctx.guild.name)

	eventObject = Event(eventName, roster, dateString, ctx.guild.id)
	activeDB["events"].update({eventName : eventObject})
	eventList.update({eventObject.eventName : eventObject})

	pushDB(activeDB)
	response = "Added " + str(len(roster)) + " players to roster"
	await ctx.send(response)


# Command implicitly takes the username of a users scheduled games, if any passed, and prints their schedule
@bot.command(name="view_schedule")
async def view_schedule(ctx):
	inputString = str(ctx.message.content)
	# Command when no implicit argument
	if len(inputString) == 16:
		response = "There are currently " + str(len(eventList)) + " matches scheduled:"
		await ctx.send(response)
		for event in eventList.keys():
			eventObject = eventList[event]
			response = event + "on " + str(eventObject.time)
			await ctx.send(response[0:-3])


	# Command when implicit argument
	else:
		pass


@bot.command(name="add_server_to_db")
async def add_server_to_db(ctx):
	DBname = str(ctx.guild)
	activeDB = pullDB(DBname)
	if activeDB == None:
		await ctx.send("Failed to construct DB")
		return None

	for member in ctx.guild.members:
		if member != bot.user:
			name = str(member)
			activeDB["players"].update({name : Player(name, [str(member.name)])})

	await ctx.send("Finished processing server users...\nDB entries:")
	await ctx.send(activeDB)
	pushDB(activeDB)
	

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
	user = await findPlayer(ctx, username)
	if user == None:
		return None
	await rsvpForMatch(ctx, user)
	response = "Created RSVP channel for " + idToPingableString(user.id)
	await ctx.send(response)


@bot.command(name="resolve_player")
async def resolvePlayer(ctx, name):
	response = await findPlayer(ctx, name)
	if response != None:
		await ctx.send(response)


# Helper Functions

async def rsvpForMatch(ctx, user):
	takenChannels = len(openSecretChannels)
	newChannelName = "Match-RSVP-" + str(takenChannels+1)
	openSecretChannels.append(newChannelName)

	channel = await ctx.guild.create_text_channel(newChannelName)

	#sets perms
	everyone = ctx.guild.roles[0]
	await channel.set_permissions(everyone, view_channel=False)
	await channel.set_permissions(user, view_channel=True)


async def trimOldChannels():
	total = 0
	for server in bot.guilds:
		for channel in server.channels:
			if len(channel.name) >= 11:
				if channel.name[0:10] == "match-rsvp":
					print("Trimmed", channel, "from", channel.guild)
					await channel.delete(reason="leftover channel")
					total += 1
	print("Finished trimming", total, "leftover channels")

def setupTimeThread():
	for guild in bot.guilds:
		activeDB = pullDB(guild.name)
		print(guild.name, "'s Database\n", activeDB)
		for event in activeDB["events"]:
			eventList.update({event : activeDB["events"][event]})


	eventThread = EventThread(bot, eventList)
	eventThread.start()
	print(eventList)



# Runner

bot.run(tokenFile["token"])