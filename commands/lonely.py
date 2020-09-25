from extras.request import Request
from extras.answers import answer, error

async def run(context):

    request = Request(context)
    authorInVoice = request.context.author.voice

    if not authorInVoice:
        await error(request, "isNotInVoice")
    elif len(authorInVoice.channel.members) != 1:
        await error(request, "isNotLonely")
    else:
        await answer(request, "isLonely", request.author.name, authorInVoice.channel)