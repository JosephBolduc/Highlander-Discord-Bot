# simul execution for checking the date and time
import threading
import time
from ShelveDB import *

# A class that manages its own thread to run an event loop
class EventThread(object):
	# Hmm, today I will write thread-unsafe code...
	def __init__(self, bot, eventList):
		self.bot = bot
		self.eventList = eventList

		self.catBox = {}         # Stores all events
		self.virgil = {}    # Events approaching one day
		self.beatrice = {}  # Events approaching one hour
		self.clairvaux = {} # Events approaching ten minutes

		self.guildList = [] # List of API guild objects
		for guild in bot.guilds:
			self.guildList.append(guild)

		for key in eventList.keys():
			self.virgil.update({key : eventList[key]})

		def threadTarget(virgil, beatrice, clairvaux, catBox, eventList):
			while True:
				time.sleep(10)
				virgil.update(eventList)
				if "kill" in virgil.keys():
					virgil.clear()
					beatrice.clear()
					clairvaux.clear()
					catBox.clear()
					self.eventList.pop("kill")
					break
				catBox.clear()
				catBox.update(virgil)
				catBox.update(beatrice)
				catBox.update(clairvaux)
				print("Activated in thread!")

		self.thread = threading.Thread(target=threadTarget, args=(self.virgil, self.beatrice, self.clairvaux, self.catBox, self.eventList))

	def start(self):
		self.thread.start()

