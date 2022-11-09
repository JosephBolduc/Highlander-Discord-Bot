import discord
from discord.ext import commands
import random

class ChatReactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bombs = ["bomb", "explosive", "explode", "c4", "payload cart"]

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


    def terrorize(self):
        maps = ["pl_badwater", "pl_barnblitz", "pl_borneo", "pl_swiftwater", "pl_upward",
                "pl_thundermountain", "pl_snowycoast", "plr_bananabay", "plr_hightower"]
        cart = ["payload", "bomb", "cart"]

        response = ""
        if random.randint(1,3) == 1:
            response += "Ok so imagine "

        response += maps[random.randint(0, len(maps) - 1)] + " but instead I push the " + cart[random.randint(0, len(cart) - 1)] + " into your house."

        if random.randint(1,2) == 1:
            response = response.lower()
            if random.randint(1,2) == 1:
                response = response[0:-1]

        elif random.randint(1,40) == 1:
            response = response.upper()

        return response

    def zaza(self):
        return "When you outside and smell that zaza breh."