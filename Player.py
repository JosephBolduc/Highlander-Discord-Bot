import json
class Player():
    def __init__(self, name, roles, aliases):
        self.name = name       # String for their discord uID
        self.aliases = aliases # List of aliases that can be added by the person or admin
        self.roles = roles     # List that contains the players server roles

    def jsonify(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        result = "Player Name: " + self.name + "\n"

        result += "Aliases: "
        for item in self.aliases:
            result += item + ", "
        result += "\n"

        result += "Other Roles: "
        for item in self.roles:
            result += item + ", "

        return str(result)