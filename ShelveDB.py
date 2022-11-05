import shelve
# Shelve DB Functions

# Removes illegal characters from strings
def fixString(string):
	illegal = "!@#$%^&*()[]{}/\\:;'\" +=`~"
	stringBuilder = ""
	for character in string:
		if character not in illegal:
			stringBuilder += character
	return stringBuilder
	

# Either creates a new shelf with the given name or returns a copy of the opened shelf
def pullDB(name):
	try:
		copyDB = {}
		name = fixString(name)

		with shelve.open("shelves\\"+name) as db:
			keyNums = 0
			for item in db.keys():
				keyNums += 1

			if keyNums == 0:
				db["name"] = name
				db["players"] = {}
				db["events"] = {}
				print("Created", db["name"], "to disk")

			for key in db.keys():
				copyDB[key] = db[key]

		print("Copied", copyDB["name"], "to memory")
		return copyDB
	except:
		print("Failed to read", name, "from disk")


# Stores a dictionary to a shelf
def pushDB(copyDB):
	try:
		with shelve.open("shelves\\"+copyDB["name"]) as db:
			for key in copyDB.keys():
				db[key] = copyDB[key]
			print("Wrote", db["name"], "to disk")

	except:
		print("Failed to write", copyDB["name"], "to disk!")