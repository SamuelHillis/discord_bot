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

        cmd = argc[0]
        argc = list(argc[1:])
        if (cmd == "add"):
            await self.add_character(ctx, argc)
        elif (cmd == "set"):
            await self.set_character(ctx, argc)
        elif (cmd == "remove"):
            await self.del_character(ctx, argc)
        elif (cmd == "view"):
            await self.view_characters(ctx, ctx.message.author)
        else:
            argc.insert(0, cmd)
            await self.get_character(ctx, argc)


    async def add_character(self, ctx, argc):
        if (len(argc) < 2):
            await ctx.send("Usage: character add [Character Name]")
            return

        name = " ".join(argc)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Character (PlayerID, Name)
            VALUES (?, ?)
        """, (ctx.message.author.id, name,))

        await ctx.send(f"Added {name} to {ctx.message.author}'s characters!")
        conn.commit()
    

    async def del_character(self, ctx, argc):
        if (len(argc) < 2):
            await ctx.send("Usage: character remove [Character Name]")
            return

        name = " ".join(argc)
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM Character
            WHERE PlayerID == ? AND Name == ?
        """, (ctx.message.author.id, name,))

        if (cur.fetchone() != None):
            await ctx.send(f"{name} has been deleted!")
        else:
            await ctx.send(f"You don't have a character named {name}!")
        conn.commit()


    async def view_characters(self, ctx, member: Member):
        if (member == None):
            await ctx.send("I don't know who that is...")
            return

        cur = conn.cursor()
        cur.execute("""
            SELECT Name FROM Character
            WHERE PlayerID == ?
        """, (member.id,))

        chars = cur.fetchall()
        out = ""

        if (len(chars) > 0):
            out += f">>> {member}'s characters are:\n "
            for c in chars:
                out += c[0] + "\n"
            out.strip()
        else:
            out += f"{member} has no characters!"

        await ctx.send(out)

    
    async def get_character(self, ctx, argc):
        if (len(argc) == 0):
            await ctx.send("Please give me a character name!")
            return

        name = " ".join(argc)
        cur = conn.cursor()
        cur.execute(f"""
            SELECT Description FROM Character
            WHERE PlayerID == ? AND Name == ?
        """, (ctx.message.author.id, name))

        character = cur.fetchone()
        
        if (character == None):
            await ctx.send(f"No character named {name}!")
        else:
            await ctx.send(f">>> **{name}**\n{character[0]}")


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
