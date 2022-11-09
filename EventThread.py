# simul execution for checking the date and time
import threading
import time

# A class that manages its own thread to run an event loop
class EventThread(object):
    # Hmm, today I will write thread-unsafe code...
    def __init__(self, bot, eventList):
        self.bot = bot
        self.eventList = eventList

        self.virgil = {}    # Events approaching one day
        self.beatrice = {}  # Events approaching one hour
        self.clairvaux = {} # Events approaching ten minutes

        for item in eventList:
            self.virgil.update({item : eventList[item]})

        def threadTarget(virgil, beatrice, clairvaux):
            while True:
                time.sleep(4)
                print("Activated in thread!")

        self.thread = threading.Thread(target=threadTarget, args=(self.virgil, self.beatrice, self.clairvaux,))

    def start(self):
        self.thread.start()

