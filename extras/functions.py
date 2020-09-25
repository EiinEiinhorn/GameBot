import json

def getGlobals(variable):
    with open("additions/globals.json", "r", encoding="UTF-8") as file:
        return json.load(file)[variable]

answersPath = getGlobals("answersFilePath")

def readHelpFile():
    with open("additions/help.txt", "r", encoding="UTF-8") as file:
        return file.read()

def matchWords(wordx, wordy):
    return str(wordx).lower().strip() == str(wordy).lower().strip()

def wordInList(wordx, listx):
    return str(wordx).lower().strip() in [str(wordy).lower().strip() for wordy in listx]

def getNickNames(idList, request):
    nickNames = []
    for member in request.context.guild.members:
        if member.id in idList:
            nickNames.append(member.display_name)
    return nickNames

def getUserNameById(userID, bot):
    return bot.get_user(userID).name

def idToPings(idList):
    return " ".join(["<@!" + str(userID) + ">" for userID in idList])

def langsAvailable():
    with open(answersPath, "r", encoding="UTF-8") as file:
        return [lang for lang in json.load(file)]

def memberPlays(member, name):
    for activity in member.activities:
        if hasattr(activity, "name"):
            if activity.name == name:
                return True
    return False