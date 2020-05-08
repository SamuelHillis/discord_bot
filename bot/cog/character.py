import discord
import sqlite3

from discord import Member
from discord.ext.commands import (
    Cog, Context,
    command
)

from bot import Bot
from constants import conn


def Characters(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="character")
    async def character(self, ctx, *argc):
        if (len(argc) == 0):
            get_character(ctx.message.author)
            return

        cmd = argc.remove(0)
        elif (cmd == "add"):
            add_character(argc)
        elif (cmd == "set"):
            set_character(argc)
        elif (cmd == "remove"):
            del_character(argc)
        else:
            member = " ".join(argc)
            get_character(member)


    def get_character(self, member: Member):
        if (member == None):
            await ctx.send("I don't know who that is...")
            return

        cur = conn.cursor()
        

        cur.execute(f"""
            SELECT Name, Description FROM Character
            WHERE PlayerID == ?
        """, (member.id,)

        out = f"{member}'s characters are:\n")

        for c in cur.fetchall():
            out = out + "> " + c[0] + "\t" + c[1] + "\n"

        await ctx.send(out[:-2])


def setup(bot: Bot) -> None:
    conn.cursor().execute("""
            CREATE TABLE IF NOT EXISTS Character (
                ID          INTEGER PRIMARY KEY     AUTOINCREMENT,
                PlayerID    INTEGER NOT NULL,
                Name        TEXT    NOT NULL,
                Description TEXT    DEFAULT 'No description'
            )
    """);
    bot.add_cog(Characters(bot))

    
