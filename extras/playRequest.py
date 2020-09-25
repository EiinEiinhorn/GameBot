from extras.functions import getGlobals, idToPings
from extras.request import playProcess
from extras.answers import Answer
import asyncio

maxTimer = getGlobals("maxCountdownMinutes")
maxPassed = getGlobals("maxMinutesForPlayAdd")
serverdata = getGlobals("serverFilePath")


async def playRequest(request, result, *args):

    process = playProcess(request, result, *args)
    await process.sendMessage()

    while process.currentMinutes:

        # if str(request.playRequestId) not in getAllPlayRequests(request.context):
        #     break

        await process.editMessage()
        await process.sleep(1)
        process.currentMinutes -= 1

    else:

        if process.minutes:
            await process.response.delete()
            process.args = [f"{process.args[0]} {idToPings([request.author.id])}"] + list(process.args[1:])
            await process.sendMessage()
        
        await asyncio.sleep(maxPassed * 60)


    answer = process.getAnswer().split("\n", 1) 
    question = answer[0].rsplit("?", 1)[0] + "?"
    userList = "\n" + answer[1]
    process.edit.remove()

    # if process.currentMinutes:
    #     question += Answer(request, "cancelled").answerString(structure=" `{}`")
    #     await process.response.edit(content = question)
    # else:
    #     process.edit.remove()
    #     await process.response.edit(content = (question + userList))

    await process.response.edit(content = (question + userList))