class Player():
    def __init__(self, name, aliases):
        self.name = name       # String for their discord uID
        self.aliases = aliases # List of aliases that can be added by the person or admin
        self.schedule = {
                "yyyy-mm-dd": True  # Used for storing if a player can make it to a game or not, takes a date as a key and True or False if they could or couldn't make it
            }

    def __str__(self):
        result = "Player Name: " + self.name + "\n"

        result += "Aliases: "
        for item in self.aliases:
            result += item + ", "
        result += "\n"

        return str(result)