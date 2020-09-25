from extras.request import Request
from extras.answers import answer

async def run(context):
    
    request = Request(context)
    values = request.message.values

    if await request.message.validateInput(values):
        request.server.file.addGroup(values[0], values[1:], request.author.id)
        await answer(request, "groupCreated", values[0])