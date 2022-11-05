# Random Helper Functions

def idToPingableString(id):
	response = "<@" + str(id) + ">"
	return response


# Resolves a player input into a player object
async def findPlayer(ctx, name):
	if type(name) != str:
		return name
	if name[0] == "<" and name[-1] == ">":
		name = name[2:-1]
		user = await ctx.guild.fetch_member(int(name))
		return user

	# Resolve by self identifier
	synonymsForMe = ["me", "self", "myself"]
	if name in synonymsForMe:
		return ctx.author

	# Resolve by nickname
	search = ctx.guild.get_member_named(name)
	if search != None:
		return search

	# Resolve by name
	memberList = ctx.guild.members
	for member in memberList:
		if member.name == name:
			return member

	await ctx.send("Could not resolve name")
	return None