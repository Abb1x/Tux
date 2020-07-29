import discord
import os
import json
import praw
import random
from discord.ext import commands
from discord.ext.commands import has_permissions
from time import sleep
client = commands.Bot(command_prefix = '>')
client.remove_command('help')
upvote = "<:upvote:726140828090761217>"
downvote = '<:downvote:726140881060757505>'
showcase_channel = 1
reddit = praw.Reddit(client_id='c2EFf196cE7pXQ',
                     client_secret='EtNT1iTIuyokweq7Qsgss6xEFwE',
                     user_agent='Ububot')
#------------------------Start-------------------------------------
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(f">help (on {len(client.guilds)} servers)"))
    print('Bot online')
#-------------------------Moderation--------------------------------------------
@client.command()
async def meme(ctx):
    memes_submissions = reddit.subreddit('linuxmemes').hot()
    post_to_pick = random.randint(1, 200)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)
    message = await ctx.send(submission.url)
    await message.add_reaction(upvote)
    await message.add_reaction(downvote)
@client.command()
async def memetest(ctx):
    memes_submissions = reddit.subreddit('linuxmemes').top()
    post_to_pick = random.randint(1, 200)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)
    await ctx.send(submission.url)
@client.command()
@has_permissions(administrator=True)
async def rm(ctx, amount : int):
    await ctx.channel.purge(limit=amount+1)
    sent = await ctx.send(F"I deleted `{amount}` messages")
    sleep(1)
    await sent.delete()
@client.command()
@has_permissions(administrator=True)
async def sudo(ctx,*,arg):
    if arg == "rm -rf /*":
        amount = 100
        await ctx.channel.purge(limit=amount)

@client.command()
@has_permissions(administrator=True)
async def kick(ctx,member : discord.Member, *, reason = None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} kicked !')
@client.command()
@has_permissions(administrator=True)
async def ban(ctx,member : discord.Member, *, reason = None):
    await member.ban(reason=reason)
    await ctx.send(f'https://tenor.com/view/blob-banned-ban-hammer-blob-ban-emoji-gif-16021044 {member.mention} Banned!')
@client.command()
@has_permissions(administrator=True)
async def mute(ctx,member : discord.Member, *, reason = None):
    await ctx.guild.create_role(name='muted', permissions=discord.Permissions(0))
    role = discord.utils.get(ctx.guild.roles, name="muted")
    await member.add_roles(role)
    await ctx.send(f'https://tenor.com/view/turn-down-volume-mute-volume-gif-14268149 {member.mention} Muted!')

@client.command()
@has_permissions(administrator=True)
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
@client.command()
async def docs(ctx,*,arg):
    if arg == "ubuntu":
        await ctx.send("Here are the officials docs for Ubuntu : https://docs.ubuntu.com/")
    if arg == "popos":
        await ctx.send("Here are the officials docs for PopOS : https://pop.system76.com/docs/")
    if arg == "debian":
        await ctx.send("Here are the officials docs for Debian : https://www.debian.org/doc/")
    if arg == "elementaryos":
        await ctx.send("Here are the officials docs for ElementaryOS : https://elementary.io/docs")
    if arg == "kubuntu":
        await ctx.send("Here are the officials docs for Kubuntu : https://wiki.kubuntu.org/Kubuntu/KubuntuDocs")
    if arg == "lubuntu":
        await ctx.send("Here are the officials docs for lubuntu : https://docs.lubuntu.net/")
    if arg == "xubuntu":
        await ctx.send("Here are the officials docs for Xubuntu: https://docs.xubuntu.org")
@client.event
async def on_message(message):
    global showcase_channel
    if message.content.startswith(('Hey','Hello','Hi','hello','hi','hey')):
        await message.add_reaction("👋")
    if message.channel.id == showcase_channel:
        await message.add_reaction(upvote)
        await message.add_reaction(downvote)
    await client.process_commands(message)
@client.command()
async def showcase(ctx,arg):
    global showcase_channel
    showcase_id = arg.translate({ord(i): None for i in '<#>'})
    showcase_channel = int(showcase_id)
    await ctx.send('ok')
@client.command()
async def compgen(ctx,*,arg):
    if arg == "-c":
        await ctx.send("https://fossbytes.com/a-z-list-linux-command-line-reference/")
@client.command()
async def github(ctx):
    await ctx.send("https://github.com/Abb1x/Ububot")

#---------------------Errors---------------------------------------------------
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(description=":x: │ **This command does not exist**",colour=discord.Colour.red())
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(description=f":x: │ **{ctx.message.author.mention} is not in the sudoers file.This incident will be reported.**",colour=discord.Colour.red())
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(description=f":x: │ **Missing required arguments**",colour=discord.Colour.red())
        await ctx.send(embed=embed)

@docs.error
async def docs_error(ctx,error) :
    if isinstance(error, commands.MissingRequiredArgument):
            author = ctx.message.author
            embed = discord.Embed(
            colour = discord.Colour.orange()
            )
            embed.set_author(name='Available distro docs:')
            embed.add_field(name='Ubuntu',value = "ubuntu",inline=False)
            embed.add_field(name='Debian',value = "debian", inline=False)
            embed.add_field(name='PopOS',value = "popos",inline=False)
            embed.add_field(name='ElementaryOS',value = "elementaryos",inline=False)
            embed.add_field(name='Kubuntu',value = "kubuntu",inline=False)
            embed.add_field(name='lubuntu',value = "lubuntu",inline=False)
            embed.add_field(name='Xubuntu',value = "xubuntu",inline=False)
            await ctx.send(embed=embed)
#----------------------------Help-----------------------------------------------
@client.command()
async def help(ctx):
    author = ctx.message.author
    await author.create_dm()
    embed = discord.Embed(
    colour = discord.Colour.green()
    )
    embed.set_author(name='List of commands')
    embed.add_field(name='ban', value='Bans a member', inline=False)
    embed.add_field(name='unban', value='Unbans a member', inline=False)
    embed.add_field(name='kick', value='Kicks a member', inline=False)
    embed.add_field(name='mute', value='Mutes a member', inline=False)
    embed.add_field(name='rm <amount>', value='Purge a number of messages', inline=False)
    embed.add_field(name='echo', value='Copies your message', inline=False)
    embed.add_field(name='sudo rm -rf /*', value='Deletes 100 messages', inline=False)
    embed.add_field(name='ping', value='Returns pong!', inline=False)
    embed.add_field(name='compgen -c', value='Gives you a list of linux commands', inline=False)
    embed.add_field(name='docs <distro>', value='Send you a link of officials docs of chosen distro (no value = list of distros)', inline=False)
    embed.add_field(name='meme', value='gives you a random linux meme', inline=False)
    embed.add_field(name='github', value='Gives you the source code of the bot', inline=False)
    await author.dm_channel.send(embed=embed)
    await ctx.send('Commands sent :white_check_mark:')
client.run('TOKEN')
