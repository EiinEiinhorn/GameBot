from extras.request import Request
from extras.answers import answer, error
from extras.functions import langsAvailable, wordInList


async def run(context):

    request = Request(context)
    langs = langsAvailable()

    if wordInList(request.content, langs):
        request.server.file.modify("Language", request.content.lower())
        await answer(request, "changed")
    else:
        await error(request, "languageNotFound", langs)