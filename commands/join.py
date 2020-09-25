from extras.request import Request, groupData
from extras.answers import replace, error
from extras.functions import matchWords


async def run(context):

    request = Request(context)

    if matchWords(request.content, "all"):
        for group in request.server.groups:
            if not request.author.inGroup(group):
                request.server.file.addValue(group, "Members", request.author.id)
        await replace(request, "joinedall")

    else:
        match = await request.server.validateServerGroup(request.content)
        if match:
            if not request.author.inGroup(match):
                request.server.file.addValue(match, "Members", request.author.id)
                await replace(request, "joinedgroup", match)
            else: 
                await error(request, "authorAlreadyInGroup", match)