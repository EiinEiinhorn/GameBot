from extras.request import Request, groupData
from extras.answers import answer, error
from extras.functions import getNickNames


async def run(context):

    request = Request(context)

    if request.message.isEmpty():
        if request.server.groups:

            groupList = []

            for group in request.server.groups:

                data = groupData(request.server.file, group)
                amountOfMembers = len(data.members)

                tags = ""

                if data.tags: 
                    tags = "`#" + "` `#".join(data.tags) + "`"

                groupList.append([amountOfMembers, group, tags])

            groupList.sort(key = lambda x: x[0], reverse=True)
            await answer(request, "allgroups", [f"({x[0]}) {x[1]} {x[2]}" for x in groupList])
        
        else:
            await error(request, "noGroupsOnServer")

    else:
        match = await request.server.validateServerGroup(request.content)
        if match:
            group = groupData(request.server.file, match)
            members = getNickNames(group.members, request)
            await answer(request, "group", match, tuple(group.tags), members)