import json

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from time import sleep
from datetime import datetime
import sqlite3
import random
servers = { }
class ModCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @has_permissions(manage_messages=True)
    async def rm(self,ctx, amount : int):
        await ctx.channel.purge(limit=amount+1)
        sent = await ctx.send(F"I deleted `{amount}` messages")
        sleep(1)
        await sent.delete()
    @commands.command()
    @has_permissions(ban_members=True)
    async def ban(self,ctx,member : discord.Member, *, reason = None):
        await member.ban(reason=reason)
        await ctx.send(f'https://tenor.com/view/blob-banned-ban-hammer-blob-ban-emoji-gif-16021044 {member.mention} Banned!')
    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self,ctx,member : discord.Member, *, reason = None):
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} kicked !')
    @commands.command()
    @has_permissions(administrator=True)
    async def sudo(self,ctx,*,arg):
        if arg == "rm -rf /*":
            amount = 100
            await ctx.channel.purge(limit=amount)
    @commands.command()
    @has_permissions(ban_members=True)
    async def unban(self,ctx, *, member):

        banned_users = await ctx.guild.bans()

        for ban_entry in banned_users:

            user = ban_entry.user

            await ctx.guild.unban(user)

            await ctx.send(f'{user.mention} Unbanned!.')
    @commands.command()
    @has_permissions(manage_messages=True)
    async def mute(self,ctx,member : discord.Member, *, reason = None):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = False
        overwrite.read_messages = True
        if discord.utils.get(ctx.guild.roles, name="Muted"):
            await member.add_roles(role)
        else:
            role = await ctx.guild.create_role(name='Muted', permissions=discord.Permissions(0))
            for channel in ctx.guild.channels:
                await channel.set_permissions(role, overwrite=overwrite)
        await member.add_roles(role)
        await ctx.send(f'https://tenor.com/view/turn-down-volume-mute-volume-gif-14268149 {member.mention} Muted!')

    @commands.command(aliases=['user-info','memberinfo'])
    async def userinfo(self,ctx,member: discord.Member):
        if member.guild_permissions.administrator:
            admin = "Yes"
        else:
            admin = "No"
        if member.bot:
            bot = "Yes"
        else:
            bot = "No"
        created = member.created_at
        joined = member.joined_at
        embed=discord.Embed(title=f"{member}")
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.add_field(name="Account created", value=f"{created.strftime('%Y-%m-%d')}", inline=True)
        embed.add_field(name="Nickname", value=f"{member.nick}", inline=True)
        embed.add_field(name="ID", value=f"{member.id}", inline=True)
        embed.add_field(name="Joined at", value=f'{joined.strftime("%Y-%m-%d")}', inline=True)
        embed.add_field(name="Is Admin",value=f'{admin}', inline=True)
        embed.add_field(name="Is Bot",value=f'{bot}', inline=True)
        embed.add_field(name=f'Roles', value=f'{len(member.roles)}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['server-info','guild-info'])
    async def server(self,ctx):
        nbr_member=len(ctx.guild.members)
        nbr_text=len(ctx.guild.text_channels)
        nbr_vc=len(ctx.guild.voice_channels)
        created = ctx.guild.created_at
        embed=discord.Embed(title=f"{ctx.guild.name}",color=random.randint(0, 0xffffff))
        embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
        embed.add_field(name="Server created", value=f"{created.strftime('%Y-%m-%d')}", inline=True)
        embed.add_field(name="Text Channels", value=f"{nbr_text}", inline=True)
        embed.add_field(name="ID", value=f"{ctx.guild.id}", inline=True)
        embed.add_field(name="Voice Channels", value=f'{nbr_vc}', inline=True)
        embed.add_field(name="Owner",value=f'{ctx.guild.owner}', inline=True)
        embed.add_field(name="Members",value=f'{nbr_member}', inline=True)
        embed.add_field(name=f'System Channel',value=f'{ctx.guild.system_channel}',inline=True)
        await ctx.send(embed=embed)
    @commands.command()
    @has_permissions(manage_messages=True)
    async def unmute(self,ctx,member : discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(role)
        await ctx.send(f"{member.mention} unmuted !")
    @commands.command()
    @has_permissions(manage_messages=True)
    async def levelsys(self,ctx,arg):
        global servers

        connection = sqlite3.connect("secondary.db")
        cursor = connection.cursor()
        cursor.execute("SELECT EXISTS(SELECT 1 FROM Level WHERE server_id = ?)", (ctx.guild.id,))
        if cursor.fetchone()[0] == True:
            server_in = True
        else:
            server_in = False

        if arg == 'enable':
            if server_in == False:
                sql = "INSERT INTO Level (server_id,enabled) VALUES (?,TRUE)"
            else:
                sql = "UPDATE Level SET enabled = TRUE WHERE server_id = ?"
            cursor.execute(sql,(ctx.guild.id,))
            await ctx.message.add_reaction("✅")
        if arg == "disable":
            if server_in == False:
                sql = "INSERT INTO Level (server_id,enabled) VALUES (?,FALSE)"
            else:
                sql = "UPDATE Level SET enabled = FALSE WHERE server_id = ?"
            cursor.execute(sql,(ctx.guild.id,))

            await ctx.message.add_reaction("✅")
        connection.commit()
        connection.close()

    @commands.command()
    @has_permissions(manage_messages=True)
    async def captcha(self, ctx, arg,channel):
        global servers

        connection = sqlite3.connect("secondary.db")
        cursor = connection.cursor()
        id = int(channel.translate({ord(i): None for i in '<#>'}))
        cursor.execute("SELECT EXISTS(SELECT 1 FROM captcha WHERE server_id = ?)", (ctx.guild.id,))
        if cursor.fetchone()[0] == True:
            server_in = True
        else:
            server_in = False

        if arg == 'enable':
            if server_in == False:
                 sql = "INSERT INTO captcha (channel_id,server_id,enabled) VALUES (?,?,TRUE)"
            else:
                 sql = "UPDATE captcha SET enabled = TRUE AND channel_id = ? WHERE server_id = ?"
            cursor.execute(sql, (id,ctx.guild.id))
            await ctx.message.add_reaction("✅")
        if arg == "disable":
            if server_in == False:
                 sql = "INSERT INTO captcha (server_id,channel_id,enabled) VALUES (?,0,FALSE)"
            else:
                sql = "UPDATE captcha SET enabled = FALSE WHERE server_id = ?"
            cursor.execute(sql, (ctx.guild.id,))

            await ctx.message.add_reaction("✅")
        connection.commit()
        connection.close()
def setup(client):
    client.add_cog(ModCog(client))
