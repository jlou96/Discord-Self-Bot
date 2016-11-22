import discord
from discord.ext import commands
import datetime


def time():
    return datetime.datetime.now().strftime("[%b/%d/%Y %H:%M:%S]")

def log(type: str, message: str):
    print("{:24} {:15} {}".format(time(), type, message))

class Logging():
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if str(message.content) == "":
            content = "Image Attachement: {} {}".format(message.attachments[0]["filename"], message.attachments[0]["url"])
        else:
            content = str(message.content)
        msg = "{} | #{} | {} : {}".format(str(message.server.name), str(message.channel.name), str(message.author), str(content))
        if message.author.id == "173709318133121024" or message.author.id == "195466701360332803":
            log("[MSG SEND]", msg)
        else:
            log("[MSG RECIEVE]", msg)


def setup(bot):
    bot.add_cog(Logging(bot))
