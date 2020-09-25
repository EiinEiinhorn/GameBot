from extras.request import Request
from extras.answers import replace, error
from extras.functions import memberPlays


async def run(context):

    request = Request(context)
    member = context.author

    if not memberPlays(member, "Among Us"):
        await error(request, "notPlayingAmongUs")

    else:
        request.server.file.modify("AmongUsControl", member.id)
        await replace(request, "controlgiven")