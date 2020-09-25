from extras.request import Request, groupData
from extras.answers import answer, error
from extras.functions import wordInList


async def run(context):
    
    request = Request(context)
    values = request.message.values

    if len(values) > 1:

        match = await request.server.validateServerGroup(values[0])
        if match:

            tags = groupData(request.server.file, match).tags
                
            if wordInList("all", values[1:]):
                for tag in tags:
                    request.server.file.removeValue(match, "Tags", tag)
                await answer(request, "removedall", match)

            else:
                for tag in values[1:]:
                    if tag in tags:
                        request.server.file.removeValue(match, "Tags", tag)
                await answer(request, "tagremoved", match)

    else:
        await error(request, "invalidStructure")