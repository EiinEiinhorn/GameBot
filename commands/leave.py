from extras.request import Request, groupData
from extras.answers import replace, error
from extras.functions import matchWords


async def run(context):

    request = Request(context)

    if matchWords(request.content, "all"):
        for group in request.server.groups:
            if request.author.inGroup(group):
                request.server.file.removeValue(group, "Members", request.author.id)
        
        await replace(request, "leftall")
    
    else:
        match = await request.server.validateServerGroup(request.content)
        if match:
            if request.author.inGroup(match):
                request.server.file.removeValue(match, "Members", request.author.id)
                await replace(request, "leftgroup", match)
            else:
                await error(request, "authorNotInGroup", match)