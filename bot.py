import discord
import os
import dotenv
from discord.ext import commands
from time import sleep
dotenv.load_dotenv()
TOKEN = os.getenv('TOKEN')
client = commands.Bot(command_prefix = '>')
client.remove_command('help')
#------------------------Start-------------------------------------
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(">help"))
    print('Bot online')
#-------------------------Moderation--------------------------------------------
@client.command()
@commands.has_role(725739488592265227)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount)
    sent = await ctx.send(F"I deleted `{amount}` messages")
    sleep(1)
    await sent.delete()
@client.command(aliases=["sudorm-rf/*"])
@commands.has_role(725739488592265227)
async def rm(ctx):
    amount = 100
    await ctx.channel.purge(limit=amount)

@client.command()
@commands.has_role(725739488592265227)
async def kick(ctx,member : discord.Member, *, reason = None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} kicked')
@client.command()
@commands.has_role(725739488592265227)
async def ban(ctx,member : discord.Member, *, reason = None):
    await member.ban(reason=reason)
    await ctx.send(f'https://tenor.com/view/blob-banned-ban-hammer-blob-ban-emoji-gif-16021044 {member.mention} Banned!')


@client.command()
@commands.has_role(704109123469574165)
async def unban(ctx, *, member):

    banned_users = await ctx.guild.bans()

    for ban_entry in banned_users:

        user = ban_entry.user

        await ctx.guild.unban(user)

        await ctx.send(f'{user.mention} Unbanned!.')

@client.command()
async def ping(ctx):
    await ctx.send(f':ping_pong: Pong **{round(client.latency * 1000)}ms**')
@client.command()
async def echo(ctx, *, arg):
    await ctx.send(arg)
@client.event
async def on_message(message):
    if message.channel.id == 711646270279909386:
        await message.add_reaction("♥")
    await client.process_commands(message)
@client.command()
async def addrole(ctx):
        embed = discord.Embed(
        colour = discord.Colour.green()
        )
        embed.set_author(name='roles')
        embed.add_field(name='`1`', value='<@&725817127814037584>', inline=True)
        embed.add_field(name='`2`', value='<@&725817240968233012>', inline=True)
        embed.add_field(name='`3`', value='<@&725817167420981359>', inline=True)
        embed.add_field(name='`4`', value='<@&725817206377676852>', inline=True)
        embed.add_field(name='`5`', value='<@&725817284907499630>', inline=True)
        embed.add_field(name='`6`', value='<@&725817365849440268>', inline=True)
        await ctx.send(embed=embed)
#---------------------Errors---------------------------------------------------
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
         await ctx.send(":x: This command does not exists")
@clear.error
async def clear_error(ctx, error) :
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(":x: Please specify a number of messages to clear")
@rm.error
async def rm_error(ctx, error) :
        if isinstance(error, commands.MissingRole):
            await ctx.send(":x: Please run this command as root")
#----------------------------Help-----------------------------------------------
@client.command(pass_context = True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(
    colour = discord.Colour.purple()
    )
    embed.set_author(name='Commands')
    embed.add_field(name='ban', value='Ban a member', inline=False)
    embed.add_field(name='unban', value='Unban a member', inline=False)
    embed.add_field(name='kick', value='Kick a member', inline=False)
    embed.add_field(name='clear <amount>', value='purge a number of messages', inline=False)
    embed.add_field(name='echo', value='copy your message', inline=False)
    embed.add_field(name='addrole <number> ', value='Gives you a role !', inline=False)
    embed.add_field(name='sudorm-rf/*', value='Deletes 100 messages', inline=False)
    await ctx.send(embed=embed)

client.run(TOKEN)
