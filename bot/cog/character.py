import discord
import sqlite3

from discord import Member
from discord.ext.commands import (
    Cog, Context,
    command
)

from bot import Bot
from constants import conn


class Characters(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="character")
    async def character(self, ctx, *argc):
        if (len(argc) == 0):
            await self.get_character(ctx, ctx.message.author)
            return

        cmd = argc.remove(0)
        if (cmd == "add"):
            await self.add_character(ctx, argc)
        elif (cmd == "set"):
            await self.set_character(ctx, argc)
        elif (cmd == "remove"):
            await self.del_character(ctx, argc)
        else:
            member = " ".join(argc)
            await self.get_character(ctx, member)


    async def get_character(self, ctx, member: Member):
        if (member == None):
            await ctx.send("I don't know who that is...")
            return

        cur = conn.cursor()
        

        cur.execute(f"""
            SELECT Name, Description FROM Character
            WHERE PlayerID == ?
        """, (member.id,))

        chars = cur.fetchall()
        out = ""

        if (len(chars) > 0):
            out += f"{member}'s characters are:\n>>> "

            for c in cur.fetchall():
                out += c[0] + ":\n" + c[1] + "\n"
            out = out[:-2]
        else:
            out += f"{member} has no characters!"

        await ctx.send(out)


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
