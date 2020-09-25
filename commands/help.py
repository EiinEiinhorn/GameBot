from extras.functions import readHelpFile

async def run(context):
    await context.send(readHelpFile())