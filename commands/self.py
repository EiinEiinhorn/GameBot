from extras.request import Request, groupData
from extras.answers import answer, error


async def run(context):
    
    request = Request(context)
    groups = []

    for group in request.server.groups:
        if request.author.inGroup(group):
            groups.append(group)
    
    if groups:
        await answer(request, "includedGroups", groups)
    else:
        await error(request, "isInNoGroup")