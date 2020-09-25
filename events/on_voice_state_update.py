from extras.functions import getGlobals
import json

async def run(member, before, after):

    if not member.voice:
        return

    if member.id != getAmongUsControl(member.voice.channel.guild.id):
        return
    
    if not playsAmongUs(member):
        return
    
    elif member.voice.self_deaf and not member.voice.mute:
        for member in member.voice.channel.members:
            await member.edit(mute=True)

    elif not member.voice.self_deaf and member.voice.mute:
        for member in member.voice.channel.members:
            await member.edit(mute=False)


def getAmongUsControl(serverID):
    filepath = getGlobals("serverFilePath").format(serverID)
    with open(filepath, "r", encoding="UTF-8") as file:
        return json.load(file)["AmongUsControl"]


def playsAmongUs(member):

    for activity in member.activities:
        if hasattr(activity, "name"):
            if activity.name == "Among Us":
                return True

    return False