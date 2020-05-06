# Made by Samuel Thomas Porter Hillis
# Created on: May 5, 2020
# Last edited: May 5, 2020

import discord
from discord.ext import commands


class Bot(commands.Bot):
    def __init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'{self.user} is running')


