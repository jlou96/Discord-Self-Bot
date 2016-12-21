import discord
from discord.ext import commands
import json
import asyncio
import inspect

# Set's bot's desciption and prefixes in a list
description = "A self bot to do things that are useful"
bot = commands.Bot(command_prefix=["`"], description=description, self_bot=True)

########################################################################################################################

@bot.event
async def on_ready():
    # Outputs login data to console
    print("---------------------------")
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print("---------------------------")

    # Outputs the state of loading the modules to the console
    # So I know they have loaded correctly
    print("Loading Modules")
    print("---------------------------")
    bot.load_extension("modules.moderation")
    print("Loaded Moderation")
    bot.load_extension("modules.admin")
    print("Loaded Admin")
    bot.load_extension("modules.tags")
    print("Loaded Tags")
    print("---------------------------")

    await bot.change_presence(afk=True, status=discord.Status.idle)

########################################################################################################################

# Ping Pong
# Testing the response of the bot
@bot.command()
async def ping():
    """Pong"""
    await bot.say("Pong")

@bot.command()
async def source():
    """Source code"""
    await bot.say("https://github.com/DiNitride/Discord-Self-Bot")

@bot.command(pass_context=True, name="eval")
async def eval_(ctx, *, code: str):
    """Evaluates a line of code provided"""
    code = code.strip("` ")
    server = ctx.message.server
    message = ctx.message
    try:
        result = eval(code)
        if inspect.isawaitable(result):
            result = await result
    except Exception as e:
        await bot.say("```py\nInput: {}\n{}: {}```".format(code, type(e).__name__, e))
    else:
        await bot.say("```py\nInput: {}\nOutput: {}\n```".format(code, result))
    await bot.delete_message(message)

@bot.command(pass_context=True)
async def massnick(ctx, nickname: str):
    """Mass nicknames everyone on the server"""
    server = ctx.message.server
    for user in server.members:
        if user.nick == None:
            nickname = "{} {}".format(nickname, user.name)
        else:
            nickname = "{} {}".format(nickname, user.nick)
        try:
            await bot.change_nickname(user, nickname)
        except discord.HTTPException:
            continue

@bot.command(pass_context=True)
async def resetnicks(ctx):
    server = ctx.message.server
    for user in server.members:
        try:
            await bot.change_nickname(user)
        except discord.HTTPException:
            continue

########################################################################################################################

##############################
## FANCY TOKEN LOGIN STUFFS ##
##############################

with open("self_token.txt") as token:
    bot.run(token.read(), bot=False)
