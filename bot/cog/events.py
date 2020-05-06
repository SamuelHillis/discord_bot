import sqlite3

from discord.ext.commands import Cog

class Events(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        print(f"{self.bot.user} is running")

#    async def on_message(self, message):
#        if (message.author == self.bot):
#            return
