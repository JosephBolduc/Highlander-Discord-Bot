import json
class Player():
    def __init__(self, name, aliases, classes, leagues, roles):
        self.name = name       # String for their discord uID
        self.aliases = aliases # List of aliases that can be added by the person or admin
        self.classes = classes # List that contains strings "Scout", "Soldier", etc...
        self.leagues = leagues # List that contains strings "UGC", "RGL", or is empty
        self.roles = roles     # List that contains strings "MailCall", "Starter", "Alternate", "Mentor"

    def jsonify(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        result = "Player Name: " + self.name + "\n"

        result += "Aliases: "
        for item in self.aliases:
            result += item + ", "
        result += "\n"

        result += "Classes: "
        for item in self.classes:
            result += item + ", "
        result += "\n"

        result += "Leagues: "
        for item in self.leagues:
            result += item + ", "
        result += "\n"

        result += "Other Roles: "
        for item in self.roles:
            result += item + ", "