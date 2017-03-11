import discord
from discord.ext import commands
import json
import asyncio
import aiohttp

# Set's bot's desciption and prefixes in a list
description = "A self bot to do things that are useful"
bot = commands.Bot(command_prefix=['self.'], description=description, self_bot=True)

###################
## Startup Stuff ##
###################

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
    bot.load_extension("modules.misc")
    print("Loaded Misc")
    bot.load_extension("modules.moderation")
    print("Loaded Moderation")
    bot.load_extension("modules.rng")
    print("loaded RNG")
    print("---------------------------")

######################
## Misc and Testing ##
######################

# Ping Pong
# Testing the response of the bot
@bot.command(pass_context=True,hidden=True)
async def ping(ctx):
    """Pong"""
    await bot.say("Pong")
    print("Ping Pong")

# Invite link to the bot server
@bot.command()
async def server():
    """The bot's server, for updates or something"""
    await bot.say("https://discord.gg/Eau7uhf")
    print("Run: Server")

# Bot's source code
@bot.command()
async def source():
    """Source code"""
    await bot.say("https://github.com/DiNitride/GAFBot")
    print("Run: Source")

@bot.command()
async def gaf_server():
    """GAF Server Invite Link"""

#################
## ADDED STUFF ##
#################

# Helper function to check if image url is valid
# Very basic function designed to work under very specific circumstances
# Don't use this for a general case
def is_valid_image_url(url):
    return url.startswith("http") and (url.endswith('.jpg') or url.endswith('.png') or url.endswith('.jpg:large') or url.endswith('.png:large'))

# Helper function to download the image data
# Thanks TR
async def download_image(image_url):
    async with aiohttp.get(image_url) as r:
        if r.status == 200:
            image_data = await r.read()
            return image_data
    return None

def try_make_images_folder():
    try:
        os.makedir('images/')
    except OSError:
        print("OSError: subdirectory images already exists")
        print("         creating new subdirectory images_dupe instead")
        try:
            os.makedir('images_dupe/')
        except OSError:
            print("OSError: subdirectory images_dupe already exists, exiting")
            exit()

# Scan last n messages for those containing images and download the image files
# kwargs: fchan=False by default, set True to enable downloading of images hosted on 4chan
@bot.command(pass_context=True)
async def dl_images(ctx, x, **kwargs):
    print("dl_images() called")
    try_make_images_folder()
    image_urls = []
    dm = ctx.message.channel
    fchan = False
    if "fchan" in kwargs:
        fchan = kwargs[fchan]
    async for m in bot.logs_from(dm, limit=int(float(x))):
        if is_valid_image_url(m.content):
            image_urls.append(m.content)
        if len(m.attachments) and is_valid_image_url(m.attachments[0]['url']):
            image_urls.append(m.attachments[0]['url'])
    with open('log.txt', 'w') as f:
        for url in image_urls:
            f.write(url + '\n')
    print("Finished logging images")
    counter = 0
    for url in image_urls:
        if ("4chan" in url or "4cdn" in url) and fchan:
            continue
        # e.g. for url="https://puu.sh/uCW58/9091a06171.png", name would be "9091a06171.png"
        tmp = url.split('/')
        name = tmp[-1]
        # write to image data to images/9091a06171.png, where images is an immediate subdirectory
        if os.path.isfile('images/' + name):
            print("{0} already exists, skipping")
            continue
        i = await download_image(url)
        if i is None:
            counter += 1
            print("Failed to download {0}".format(url))
            with open('log.txt', w) as f:
                f.write('Failed to download {0}\n'.format(url))
            continue
        with open('images/' + name, 'wb') as img:
            img.write(i)
    print("Finished downloading images, {0} total errors".format(counter))


##############################
## FANCY TOKEN LOGIN STUFFS ##
##############################

# I couldn't feed the Token through a self_token.txt file so I just hardcoded it here
bot.run("TOKEN_GOES_HERE", bot=False)
