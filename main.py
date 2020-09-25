# IMPORTS

import commands as command
import events as event
from discord.ext import commands
import discord
import tokens

# INITIALIZATION

client = commands.Bot(command_prefix=".")
client.remove_command("help")

# EVENTS 

@client.event
async def on_ready():
    event.on_ready.run()

@client.event
async def on_message(message):
    context = await client.get_context(message)
    await event.on_message.run(context)
    await client.process_commands(message)

@client.event
async def on_voice_state_update(member, before, after):
    await event.on_voice_state_update.run(member, before, after)

# COMMANDS

@client.command()
async def addtag(context):
    await command.addtag.run(context)

@client.command()
async def amongus(context):
    await command.amongus.run(context)

@client.command()
async def changename(context):
    await command.changename.run(context)

@client.command()
async def create(context):
    await command.create.run(context)

@client.command()
async def help(context):
    await command.help.run(context)

@client.command()
async def info(context):
    await command.info.run(context)

@client.command()
async def join(context):
    await command.join.run(context)

@client.command()
async def language(context):
    await command.language.run(context)

@client.command()
async def leave(context):
    await command.leave.run(context)

@client.command()
async def lonely(context):
    await command.lonely.run(context)

@client.command()
async def play(context):
    await command.play.run(context)

@client.command()
async def remove(context):
    await command.remove.run(context)

@client.command()
async def removetag(context):
    await command.removetag.run(context)

@client.command()
async def self(context):
    await command.self.run(context)
    



# TOKENS ARE TAKEN FROM NON PUBLIC FILE
clientToken = tokens.botToken()
testToken = tokens.testToken()

# client.run(clientToken)
client.run(testToken)