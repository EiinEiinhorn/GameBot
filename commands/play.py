from extras.request import Request, groupData
from extras.answers import error
from extras.functions import idToPings, wordInList
from extras.playRequest import playRequest


async def run(context):

    request = Request(context)
    request.newPlayRequest()
    values = request.message.values

    pings = []
    
    if wordInList(values[0], ["something", "anything"]):
        for group in request.server.groups:
            if request.author.inGroup(group):
                for member in groupData(request.server.file, group).members:
                    if member not in pings and member != request.author.id:
                        pings.append(member)

        if pings:
            await playRequest(request, "something", idToPings(pings))
        else:
            await error(request, "noSharedGroup")
    
    else:
        match = await request.server.validateServerGroup(values[0])
        if match:
            for member in groupData(request.server.file, match).members:
                if member != request.author.id:
                    pings.append(member)

            if pings:
                await playRequest(request, "game", idToPings(pings), match)
            else:
                await error(request, "aloneInGroup", match)
