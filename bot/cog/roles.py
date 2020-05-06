import discord
import sqlite3

from discord.ext.commands import (
    Cog, Context, 
    command, has_permissions
)

from bot import Bot
from constants import conn


def getRole(ctx, roleName):
    return discord.utils.get(
            ctx.guild.roles,
            name=roleName
    )

class Roles(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot


    @command(name="setrole")
    @has_permissions(administrator=True)
    async def common_role(self, ctx: Context, roleName=None):
        if (roleName):
            await ctx.send("Please specify a role!")
            return

        role = getRole(ctx, roleName)
        if (role == None):
            await ctx.send(f"No such role: `{roleName}`")
            return

        cur = conn.cursor()
        cur.execute(f"""SELECT * FROM Roles WHERE RoleID == {role.id}'""")

        if (len(cur.fetchall()) > 0):
            cur.execute(f"""
                DELETE FROM Roles
                WHERE RoleID == {role.id};
            """)
            await ctx.send(f"Removed {role} from the common roles")
        else:
            cur.execute(f"""
                INSERT INTO Roles (RoleID, GuildID, Authority)
                VALUES ({role.id}, {ctx.guild.id})
            """)
            await ctx.send(f"Added {role} to the common roles")

        conn.commit()


    @command(name="role")
    async def set_role(self, ctx, roleName=None):
        if (roleName == None):
            await ctx.send("Please specify a role!")
            return

        member = ctx.message.author
        role = getRole(ctx, roleName)

        if (role == None):
            await ctx.send(f"No such role: `{roleName}`")
            return

        cur = conn.cursor()
        cur.execute(f"""
            SELECT * FROM Roles
            WHERE RoleID == {role.id};
        """)

        if (len(cur.fetchall()) == 0):
            await ctx.send(f"I cant do anything to {role}!")

        elif (role in member.roles):
            await member.remove_roles(role)
            await ctx.send(f"Removed the {role} role from {member}")

        else:
            await member.add_roles(role)
            await ctx.send(f"Gave the {role} role to {member}")


    @command(name="available")
    async def get_roles(self, ctx):
        #TODO Format output
        guild = ctx.guild
        cur = conn.cursor()

        cut.execute(f"""
            SELECT RoleID FROM Roles
            WHERE GuildID == {guild.id};
        """)

        roleIDs = cur.fetchall()

        if (len(roleIDs) == 0):
            await ctx.send(f"No available roles in {guild}")
        else:
            roleIDs = [r[0] for r in roleIDs]
            roles = [r for r in guild.roles if r.id in roleIDs]
            await ctx.send(roles)


def setup(bot: Bot) -> None:
    conn.cursor().execute("""
            CREATE TABLE IF NOT EXISTS Roles (
                RoleID INTEGER PRIMARY KEY,
                GuildID INTEGER NOT NULL
            ); 
    """)
    bot.add_cog(Roles(bot))
