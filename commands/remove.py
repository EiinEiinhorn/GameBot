from extras.request import Request
from extras.answers import answer, error


async def run(context):
    
    request = Request(context)

    if await request.message.validateNotEmpty():

        match = await request.server.validateServerGroup(request.content)
        if match:
            request.server.file.removeGroup(match)
            await answer(request, "groupRemoved", match)