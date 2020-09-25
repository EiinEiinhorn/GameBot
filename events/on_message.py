from extras.request import Request, editRequests
import re

async def run(context):

    request = Request(context)

    validFormat = re.search(r"^(\++?|\-+?)\d*?$", request.message.content)
    if validFormat:

        request.findPlayRequest()
        
        message = await request.play.findRequestMessage()
        if message:
            
            accepted = False
            if request.message.content.startswith("+"):
                accepted = True  

            edit = editRequests(request)
            edit.addUser(accepted)
            await edit.overwriteRequest(message)

            await context.message.delete()