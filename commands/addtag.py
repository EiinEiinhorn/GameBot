from extras.request import Request
from extras.answers import answer, error


async def run(context):
    
    request = Request(context)
    values = request.message.values

    if await request.message.validateInput(values[1:]):

        if len(values) > 1:

            match = await request.server.validateServerGroup(values[0])
            if match:

                for tag in values[1:]:
                    request.server.file.addValue(match, "Tags", tag)
                await answer(request, "tagadded", match)

        else:
            await error(request, "invalidStructure")