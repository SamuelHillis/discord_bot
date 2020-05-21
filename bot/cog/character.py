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
            await ctx.send("Usage: character {add|set|remove|view} {info}")
            return

        cmd = argc.remove(0)
        if (cmd == "add"):
            await self.add_character(ctx, argc)
        #elif (cmd == "set"):
        #    await self.set_character(ctx, argc)
        elif (cmd == "remove"):
            await self.del_character(ctx, argc)
        elif (cmd == "view"):
            await self.view_characters(ctx, ctx.message.author)
        else:
            await ctx.send("Add command options")


    async def add_character(self, ctx, argc):
        if (len(argc) < 2):
            await ctx.send("Usage: character add [Character Name]")
            return

        name = " ".join(argc)
        cur = conn.cursor()
        cur.execute(f"""
            INSERT INTO Character VALUES (PlayerID, Name)
            (?, ?)
        """, (ctx.message.author.id, name))

        await ctx.send(f"Added {name} to {ctx.message.author}'s characters!")


    async def del_character(self, ctx, argc):
        if (len(argc) < 2):
            await ctx.send("Usage: character remove [Character Name]")
            return

        name = " ".join(argc[1:])
        cur = conn.cursor()
        cur.execute(f"""
            DELETE FROM Character
            WHERE PlayerID == ? AND Name == ?
        """, (ctx.message.author.id, name))

        if (cur.fetchone() > 0):
            await ctx.send(f"{name} has been deleted!")
        else:
            await ctx.send(f"You don't have a character named {name}!")



    async def view_characters(self, ctx, member: Member):
        if (member == None):
            await ctx.send("I don't know who that is...")
            return

        cur = conn.cursor()
        cur.execute(f"""
            SELECT Name FROM Character
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
