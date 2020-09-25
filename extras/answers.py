from extras.functions import getGlobals
import asyncio
import json
import re


deletionTimer = getGlobals("timeBeforeErrorDeletion")
answersPath = getGlobals("answersFilePath")


async def answer(request, result, *args):

    answer = Answer(request, result, *args)
    await answer.send()


async def error(request, result, *args):

    request.message.command = "error"
    answer = Answer(request, result, *args)
    response = await answer.send(structure="_{}_")

    await asyncio.sleep(deletionTimer)
    await request.message.delete()
    await response.delete()


async def replace(request, result, *args):

    answer = Answer(request, result, *args)
    answer.args.insert(0, request.author.id)

    await answer.send(replace=True)
    await request.message.delete()



class Answer():

    def __init__(self, request, result, *args):

        self.request = request
        self.command = request.message.command
        self.language = request.server.file.getLanguage()
        self.args = []

        self.answer = self.getAnswer(result)
        self.filterArgumentBrackets()
        self.formatArguments(list(args))

    # Automatically

    def getAnswer(self, result):
        with open(answersPath, "r", encoding="UTF-8") as file:
            answers = json.load(file)
            for lang in answers:
                if lang == self.language:
                    return answers[lang][self.command][result]
    
    def filterArgumentBrackets(self, replace=False):
        for arg in re.findall(r"\{[A-Z]*?\}", self.answer):
            self.answer = self.answer.replace(arg[1:-1], "")
    
    def formatArguments(self, arguments):

        for arg in arguments:

            if arg:
                if type(arg) == list: self.args.append("\n• " + "\n• ".join(arg))
                elif type(arg) == tuple: self.args.append(" `#" + "` `#".join(arg) + "`")
                else: self.args.append(str(arg).strip())
            else: 
                self.args.append("")
    
        return self.args
    
    # On call

    def filterReplacableStrings(self, replace=False):

        replacableStrings = re.findall(r"\(\(.+?\|\|.+?\)\)", self.answer)

        for param in replacableStrings:
            replacedParameter = param[2:-2].split("||")[int(replace)]
            self.answer = self.answer.replace(param, replacedParameter)

        return self.answer
    
    def answerString(self, structure = "{}", replace=False):
        self.filterReplacableStrings(replace)
        response = self.answer.format(*self.args)
        return structure.format(response)

    async def send(self, structure = "{}", replace=False):
        answer = self.answerString(structure=structure, replace=replace)
        return await self.request.context.send(answer)