import discord
from discord.ext import commands
import json
import asyncio
import inspect

# Set's bot's desciption and prefixes in a list
description = "A self bot to do things that are useful"
bot = commands.Bot(command_prefix=['self.', "s."], description=description, self_bot=True)


ready_modules = {
    "moderation": "Moderation"
}

live_modules = {}

########################################################################################################################

@bot.event
async def on_ready():
    # Outputs login data to console
    print("---------------------------")
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print("---------------------------")

    with open("config/load-config.json") as file:
        bot.load_config = json.load(file)

    with open("config/config.json") as file:
        bot.config = json.load(file)

    # Outputs the state of loading the modules to the console
    # So I know they have loaded correctly
    print("Loading Modules")
    print("---------------------------")

    if bot.load_config["moderation"] == True:
        bot.load_extension("modules.moderation")
        live_modules["moderation"] = "Moderation"
        print("loaded Moderation")

    print("---------------------------")

    await bot.change_presence(afk=True, status=discord.Status.idle)

    asyncio.Task(save_configs())

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

########################################################################################################################

## Module loading and unloading
@bot.command()
async def load(extension_name: str):
    """Loads an extension."""
    extension_name = extension_name.lower()
    load_extension_name = "modules." + extension_name

    try:
        bot.load_extension(load_extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return

    live_modules.append(extension_name)
    bot.load_config[extension_name] = True
    await bot.say("{} loaded.".format(extension_name))

@bot.command()
async def unload(extension_name: str):
    """Unloads an extension."""
    extension_name = extension_name.lower()
    unload_extension_name = "modules." + extension_name

    if extension_name in live_modules:

        bot.unload_extension(unload_extension_name)
        bot.load_config[extension_name] = False
        await bot.say("{} unloaded.".format(extension_name))

    else:
        await bot.say("Could not unload module, module not loaded.\nTo see loaded modules, do s.loaded")

@bot.command()
async def loaded():
    output = "```Loaded Modules:"
    for x in live_modules:
        output += "\n- {}".format(ready_modules[x])
    output += "```"
    await bot.say(output)

# Config save loop
async def save_configs():
    while True:
        save = json.dumps(bot.config)
        with open("config/config.json", "w") as file:
            file.write(save)
        save = json.dumps(bot.load_config)
        with open("config/load-config.json", "w") as file:
            file.write(save)
        await asyncio.sleep(5)

########################################################################################################################

##############################
## FANCY TOKEN LOGIN STUFFS ##
##############################

with open("self_token.txt") as token:
    bot.run(token.read(), bot=False)
