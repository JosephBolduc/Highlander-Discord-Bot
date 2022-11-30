import discord
from discord.ext import commands
import random


class ChatReactions(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.bombs = [
			"bomb",
			"explosive",
			"explode",
			"c4",
			"payload cart",
			"semtex",
			"tatp",
			"urea nitrate",
			"triacetone triperoxide",
			"tannerite",
			"academy sports and outdoors",
		]
		self.targetedUsers = [
			254661838497644544,
			241958250931683329
		]

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author == self.bot.user:
			return None

		messageText = str(message.content).lower()
		if "zaza" in messageText:
			await message.reply(self.zaza())
			return None

		for item in self.bombs:
			if item in messageText:
				await message.reply(self.terrorize())
				return None

		if "troll" in messageText:
			await message.reply(self.trollingStone())
			return None

		if message.author.id in self.targetedUsers:
			if random.randint(1,5) == 1:
				await message.channel.send(self.randomReactGif())
				return None

	def terrorize(self):
		maps = [
			"pl_badwater",
			"pl_barnblitz",
			"pl_borneo",
			"pl_swiftwater",
			"pl_upward",
			"pl_thundermountain",
			"pl_snowycoast",
			"plr_bananabay",
			"plr_hightower",
		]
		cart = ["payload", "bomb", "cart"]

		response = ""
		if random.randint(1, 3) == 1:
			response += "Ok so imagine "

		response += (
			maps[random.randint(0, len(maps) - 1)]
			+ " but instead I push the "
			+ cart[random.randint(0, len(cart) - 1)]
			+ " into your house."
		)

		if random.randint(1, 2) == 1:
			response = response.lower()
			if random.randint(1, 2) == 1:
				response = response[0:-1]

		elif random.randint(1, 25) == 1:
			response = response.upper()

		return response

	def zaza(self):
		return "When you outside and smell that zaza breh."

	def randomReactGif(self):
		reactionGifs = [
			"https://media.discordapp.net/attachments/528793773346652160/1000667563715481600/F054CF2C-9261-4662-898F-4481D9E65662.gif",
			"https://media.discordapp.net/attachments/992510545997615145/1042905544828133527/popoki.gif",
			"https://media.discordapp.net/attachments/951154860412268624/1038958172796375060/attachment-1.gif",
			"https://media.discordapp.net/attachments/970524905634398258/1043377088343855114/image0_36508163147553.gif",
			"https://media.discordapp.net/attachments/970524905634398258/1043376755764891658/asdafa.gif",
			"https://media.discordapp.net/attachments/970524905634398258/1043379101274226698/C7724FD9-B527-4026-A5D1-A2B13D9753CD.gif",
			"https://media.discordapp.net/attachments/649814265347309578/1020017397454864404/funnt.gif",
			"https://media.discordapp.net/attachments/806714809462161478/1020093536798003220/bimplyactvity.gif",
			"https://media.discordapp.net/attachments/697671104046825533/977753307198148608/14D3DE03-80F9-4823-902A-73848B83645A.gif",
			"https://media.discordapp.net/attachments/970512579057287234/1031794357432487956/4521A477-1804-4CD2-874D-9C826DDD1A31.gif",
			"https://tenor.com/view/jerma-psycho-streamer-jerma985-jerma-sus-gif-25065540",
			"https://media.discordapp.net/attachments/813078853399478282/959886454669062214/funny.gif",
			"https://media.discordapp.net/attachments/838736235437883412/998292828910272612/94BBE4D0-73DD-4B50-868E-66C44B0464CD.gif",
			"https://media.discordapp.net/attachments/970512579321536523/1022027361161580564/4C93B042-327F-428E-BDF1-23E2C78C95DF.gif",
			"https://media.discordapp.net/attachments/811646862729150555/937444902676099122/dserver2-1.gif"
			]
		return reactionGifs[random.randint(0, len(reactionGifs)-1)]

	def trollingStone(self):
		trollingStones = [
			":trollingstone:",
			"https://cdn.discordapp.com/attachments/1037899375214592050/1047278726783709234/cum_nuts.PNG"
			]
		return trollingStones[random.randint(0, len(trollingStones)-1)]