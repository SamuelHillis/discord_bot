# Made by Samuel Thomas Porter Hillis
# Created on: May 5, 2020
# Last edited: May 5, 2020

import os
import discord

from bot import Bot
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = Bot(command_prefix=".")

bot.load_extension("commands.roles")

bot.run(TOKEN)
