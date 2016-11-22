import discord
from discord.ext import commands
import json

class Admin():
    def __init__(self, bot):
        self.bot = bot

    # Changes the bot's game
    @commands.command(pass_conext=True)
    async def status(self, *, status: str):
        """Updates the Bot's status
        Usage:
        $status This is my status"""
        # Update the bots game
        await self.bot.change_presence(game=discord.Game(name=status))
        await self.bot.say("Status updated to {}".format(status))

    @commands.command()
    async def invite(self, *server: str):
        """Creates a server invite
        Usage:
        $invite The Never Ending GAF"""
        server = discord.utils.get(self.bot.servers, name=server)
        if server is None:
            await self.bot.say("No server found")
            return
        invite = await self.bot.create_invite(server)
        await self.bot.say(invite.url)

def setup(bot):
    bot.add_cog(Admin(bot))
