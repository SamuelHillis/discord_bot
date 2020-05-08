import discord
import sqlite3

from discord.ext.commands import (
    Cog, Context,
    command
)

from bot import Bot

conn = sqlite3.connect("bot/resources/rulebook.db")

class Rulebook(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="spells")
    async def getrules(self, ctx: Cog, *argc):
        spell = " ".join(argc)
        cur = conn.cursor()

        if (spell == ""):
            cur.execute("""
                SELECT Sphere FROM Spell
                GROUP BY Sphere
            """)
            out = ""
            spheres = [s[0] for s in cur.fetchall()]
            for s in spheres:
                cur.execute(f"""
                    SELECT Title, Sphere, Level FROM Spell
                    WHERE Sphere == '{s}'
                    ORDER BY Level
                """)
                spells = [r[0] for r in cur.fetchall()]
                out = out + "\n" + s + "\n"
        
                for r in spells:
                    out = out + "> - " + r + "\n"

        await ctx.send(out)


def setup(bot: Bot) -> None:
    bot.add_cog(Rulebook(bot))
