from extras.request import Request
from extras.answers import answer, error
from extras.functions import wordInList


async def run(context):

    request = Request(context)
    values = request.message.values

    if await request.message.validateInput(values[1:]):

        if len(values) == 2:
            match = await request.server.validateServerGroup(values[0])
            if match:
                request.server.file.editGroupName(match, values[1].strip())
                await answer(request, "changed", match, values[1].strip())

        else:
            await error(request, "invalidStructure")