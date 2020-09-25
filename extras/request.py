from extras.answers import error, Answer
from extras.functions import matchWords, wordInList, getGlobals, getNickNames
import datetime
import os.path
import asyncio
import json
import re


invalidNames = getGlobals("invalidNames")
splitCharacter = getGlobals("splitCharacter")
maxTimer = getGlobals("maxCountdownMinutes")
filepath = getGlobals("serverFilePath")
messageLimit = getGlobals("messageSearchLimit")


class server():

    def __init__(self, Request):
        self.request = Request
        self.id = Request.context.guild.id
        self.name = Request.context.guild.name
        self.members = [member.id for member in Request.context.guild.members]

        self.file = serverFile(Request.context.guild)
        self.data = self.file.data
        self.groups = self.file.groups
    
    async def validateServerGroup(self, name):

        for group in self.file.groups:
            if matchWords(name, group) or wordInList(name, groupData(self.file, group).tags):
                return group

        await error(self.request, "groupNotFound", name)
        return False


class serverFile():

    def __init__(self, discordGuild):
        self.id = discordGuild.id
        self.name = discordGuild.name
        self.members = [member.id for member in discordGuild.members]
        self.path = filepath.format(self.id)

        if not os.path.isfile(self.path): 
            self.create()

        self.data = self.open()
        self.groups = self.data["Groups"]

        self.clean()
    
    # Clean at Start

    def clean(self):

        for group in self.groups:

            groupMembers = groupData(self, group).members
            usersNotOnServer = set(groupMembers) - set(self.members)

            for invalidUser in usersNotOnServer:
                self.removeValue(group, "Members", invalidUser)

        for group in self.groups.copy():

            groupIsEmpty = not groupData(self, group).members
            if groupIsEmpty:
                self.removeGroup(group)
    
    # Get Dynamic Content

    def getLanguage(self):
        return self.data["Language"]

    # Write

    def create(self):
        with open(self.path, "w", encoding="UTF-8") as file:
            file.write(json.dumps({
                "Servername": self.name, 
                "Server ID": self.id,
                "Language": "en",
                "Groups": {},
                "CurrentRequests": {},
                "AmongUsControl": 0
            }))

    def write(self):
        with open(self.path, "w", encoding="UTF-8") as file:
            file.write(json.dumps(self.data))

    def open(self):
        with open(self.path, "r", encoding="UTF-8") as file:
            return json.load(file)

    # Edit

    def editGroupName(self, old, new):
        self.data["Groups"][new] = self.data["Groups"].pop(old)
        self.write()
    
    def addGroup(self, group, tags, author):
        self.data["Groups"][group] = {"Tags": tags, "Members": [author]}
        self.write()
    
    def addValue(self, group, attr, value):
        self.data["Groups"][group][attr].append(value)
        self.write()

    def removeGroup(self, group):
        del self.data["Groups"][group]
        self.write()

    def removeValue(self, group, attr, value):
        self.data["Groups"][group][attr].pop(self.groups[group][attr].index(value))
        self.write()

    def modify(self, key, value):
        self.data[key] = value
        self.write()


class message():

    def __init__(self, Request):
        self.request = Request
        self.server = server(Request)

        message = Request.context.message.content.strip()

        if message.startswith("."):
            self.command = message[1:].split(" ")[0].strip()
            self.content = " ".join(message[1:].split(" ")[1:]).strip()
        else:
            self.command = None
            self.content = message
        
        self.values = list(map(str.strip, self.content.split(splitCharacter)))
    
    async def delete(self):
        await self.request.context.message.delete()

    def isEmpty(self):
        return not bool(self.content)

    async def validateNotEmpty(self):
        if not self.content:
            await error(self.request, "emptyMessage")
        return bool(self.content)

    async def validateNames(self, names):

        for name in names:
            if wordInList(name, invalidNames):
                await error(self.request, "invalidName", name)
                return False
        
        for group in self.request.server.groups:

            if wordInList(group, names):
                await error(self.request, "nameTaken", group)
                return False
        
            for tag in groupData(self.server.file, group).tags:
                if wordInList(tag, names):
                    await error(self.request, "nameTaken", group)
                    return False
        
        return True
    
    async def validateInput(self, names):

        if await self.validateNotEmpty():
            if await self.validateNames(names):
                return True
            
        return False


class author():

    def __init__(self, Request):
        self.id = Request.context.author.id
        self.name = Request.context.author.name
        self.server = server(Request)
    
    def inGroup(self, group):
        groupMembers = groupData(self.server.file, group).members
        return wordInList(self.id, groupMembers)


class Request():

    def __init__(self, context):
        
        self.context = context
        self.message = message(self)
        self.author = author(self)
        self.server = server(self)
        self.content = self.message.content
        self.bot = context.bot
    
    def newPlayRequest(self):
        self.play = newPlayRequest(self)
    
    def findPlayRequest(self):
        self.play = findPlayRequest(self)


class groupData():
    def __init__(self, serverfile, group):
        self.name = group
        self.members = serverfile.data["Groups"][group]["Members"].copy()
        self.tags = serverfile.data["Groups"][group]["Tags"].copy()


# PLAYREQUESTS


class playRequests():

    def __init__(self, Request):
        self.request = Request
    
    def open(self):
        with open(filepath.format(self.request.server.id), "r", encoding="UTF-8") as file:
            self.file = json.load(file)
            return self.file["CurrentRequests"]
    
    def write(self):
        with open(filepath.format(self.request.server.id), "w", encoding="UTF-8") as file:
            file.write(json.dumps(self.file))


class findPlayRequest(playRequests):

    def __init__(self, Request):
        self.request = Request
        self.content = Request.content

        self.prefix = self.content[0]
        self.id = self.getID()
        self.accepted = self.checkIfAccepted()
    
    def getID(self):
        if self.content[-1].isdigit():
            return int(self.content.rsplit(self.prefix, 1)[1])
        if self.open():
            return 0
        return None

    def checkIfAccepted(self):
        if self.prefix == "+":
            return True
        return False

    def getIDFromMessage(self, message):
        return int(message.content.split("\n", 1)[0].rsplit("`+", 1)[1].split("`", 1)[0])
    
    def minutesPassed(self, discordMessage):
        return (datetime.datetime.utcnow() - discordMessage.created_at).total_seconds() / 60

    def messageIsMatch(self, message):
        if re.search(r"`\+\d+?`", message.content):
            messageId = self.getIDFromMessage(message)
            if self.id == 0 or self.id == messageId:
                self.id = messageId
                return True
        return False

    async def getMessageHistory(self):
        maxPassedUTC = datetime.datetime.utcnow() - datetime.timedelta(minutes=maxTimer)
        return await self.request.context.channel.history(after=maxPassedUTC, oldest_first=False).flatten()
    
    async def findRequestMessage(self):
        for message in await self.getMessageHistory():
            if self.minutesPassed(message) > maxTimer:
                return False
            if message.author.id != self.request.bot.user.id:
                continue
            if self.messageIsMatch(message):
                return message
    

class newPlayRequest(playRequests):

    def __init__(self, Request):
        self.request = Request
        self.timer = self.getTimer()

        self.createRequest()

    def getTimer(self):
        if len(self.request.message.values) > 1:
            timer = self.request.message.values[1]
            if timer.isdigit():
                if int(timer) > maxTimer:
                    return maxTimer
                elif int(timer) > 0:
                    return int(timer)
        return 0
    
    def createRequest(self):

        currentRequests = self.open()

        self.id = 1
        if len(currentRequests):
            self.id = int(list(currentRequests)[-1]) + 1
        currentRequests[self.id] = {"Accepted": [self.request.author.id], "Declined": []}

        self.write()
    

class editRequests(playRequests):

    def __init__(self, Request):
        self.request = Request
        self.id = Request.play.id
    
    def remove(self):
        requests = self.open()
        del requests[str(self.id)]
        self.write()
    
    def addUser(self, accepted):
        requests = self.open()
        data = requests[str(self.id)]
        
        if accepted:
            data["Accepted"] = list(set(data["Accepted"]) | set([self.request.author.id]))
            data["Declined"] = list(set(data["Declined"]) - set([self.request.author.id]))
        else:
            data["Accepted"] = list(set(data["Accepted"]) - set([self.request.author.id]))
            data["Declined"] = list(set(data["Declined"]) | set([self.request.author.id]))
        
        self.write()
    
    async def overwriteRequest(self, botMessage):
        question = botMessage.content.split("\n", 1)[0]
        userList = self.getUserList()
        await botMessage.edit(content = (question + userList))
    
    def getUserList(self):
        requests = self.open()
        accepted = "\n✓ ".join([""] + getNickNames(requests[str(self.id)]["Accepted"], self.request))
        declined = "\n✘ ".join([""] + getNickNames(requests[str(self.id)]["Declined"], self.request))
        return accepted + declined


class playProcess():

    def __init__(self, Request, result, *args):
        self.edit = editRequests(Request)
        self.request = Request
        self.minutes = Request.play.timer
        self.currentMinutes = Request.play.timer
        self.result = result
        self.args = args

    def getAnswer(self):
        answer = Answer(self.request, self.result, *self.args)
        answer.args.append(self.getMinuteString())
        answer.args.append(self.request.play.id)
        return answer.answerString() + self.edit.getUserList()
    
    async def sendMessage(self):
        self.response = await self.request.context.send(self.getAnswer())
    
    async def editMessage(self):
        await self.response.edit(content = self.getAnswer())
    
    async def sleep(self, minutes):
        minutesPassed = datetime.timedelta(minutes=(self.minutes - self.currentMinutes + minutes))
        nextMinutePassedAt = self.response.created_at + minutesPassed
        secondsUntilNextMinute = (nextMinutePassedAt - datetime.datetime.utcnow()).total_seconds()
        await asyncio.sleep(secondsUntilNextMinute)

    def getMinuteString(self):
        if not self.currentMinutes:
            return Answer(self.request, "now").answer
        if self.currentMinutes == 1: 
            return Answer(self.request, "minutes").filterReplacableStrings(replace=True).format(self.currentMinutes)
        if self.currentMinutes != 1: 
            return Answer(self.request, "minutes").filterReplacableStrings().format(self.currentMinutes)


# display_name

# if accepted:
#         if context.author.id not in data["Accepted"]:
#             data["Accepted"].append(context.author.id)
#         if context.author.id in data["Declined"]:
#             data["Declined"].remove(context.author.id)
#     else:
#         if context.author.id in data["Accepted"]:
#             data["Accepted"].remove(context.author.id)
#         if context.author.id not in data["Declined"]:
#             data["Declined"].append(context.author.id)