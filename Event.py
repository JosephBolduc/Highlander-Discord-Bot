import datetime
from datetime import datetime

class Event():
    def __init__(self, eventName, roster, time, serverID):
        self.eventName = eventName
        dt = datetime.strptime(time, "%H:%M %d/%m/%Y") # HH:MM DD/MM/YYYY
        self.time = dt

        self.roster = {
                "uIDGoesHere": True  # Used for storing if a player can make it to a game or not, their uID and True or False if they could or couldn't make it
            }

        # Roster accepts a list of member uIDs
        for player in roster:
            self.roster.update({player: False})

        self.serverID = serverID

    def __str__(self):
        result = "Event Name: " + self.eventName + "\n"

        result += "Roster: "
        for item in self.roster.keys():
            result += item + ", "
        result += "\n"

        result += self.time + "\n"
        result += self.serverID

        return str(result)