import discord
from discord.ext import commands
import json
import asyncio

class Tags():

    def __init__(self, bot):
        self.bot = bot

        with open("config/tags.json") as file:
            self.tags = json.load(file)

        asyncio.Task(self.save_tags())

    @commands.command()
    async def rmtag(self, command: str):
        """Removes a tag
        Usage:
        self.rmtag tag"""
        if command in self.tags:
            del self.tags[command]
            await self.bot.say("Tag {} has been removed :thumbsup:".format(command))
        else:
            await self.bot.say("Tag not registered, could not delete :thumbsdown: ")

    @commands.command()
    async def tags(self):
        """Lists the tags added
        Usage:
        self.tags"""
        taglist = "```Tags:"
        for x in self.tags.keys():
            taglist = "{}\n- {}".format(taglist, x)
        await self.bot.say("{0} ```".format(taglist))

    @commands.command(pass_context=True)
    async def tag(self, ctx, input : str, *, output: str = None):
        """Adds or displays a tag
        Usage:
        self.tag tag_name tag_data
        If 'tag_name' is a saved tag it will display that, else it will
        create a new tag using 'tag_data'"""
        if input in self.tags:
            await self.bot.say(self.tags[input])
        else:
            self.tags[input] = output
            if output.startswith("http"):
                await self.bot.say("Tag {} has been added with output <{}> :thumbsup:".format(input, output))
            else:
                await self.bot.say("Tag {} has been added with output {} :thumbsup:".format(input, output))

    async def save_tags(self):
        while True:
            save = json.dumps(self.tags)
            with open("config/tags.json", "w") as data:
                data.write(save)
            await asyncio.sleep(60)

def setup(bot):
    bot.add_cog(Tags(bot))
