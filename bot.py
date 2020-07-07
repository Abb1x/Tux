import discord
import os
import praw
import random
from discord.ext import commands
from time import sleep
client = commands.Bot(command_prefix = '>')
client.remove_command('help')
upvote = "<:upvote:726140828090761217>"
downvote = '<:downvote:726140881060757505>'
reddit = praw.Reddit(client_id='ID',
                     client_secret='SECRET',
                     user_agent='Ububot')
#------------------------Start-------------------------------------
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(">help"))
    print('Bot online')
#-------------------------Moderation--------------------------------------------
@client.command()
async def meme(ctx):
    channel = client.get_channel(711647460937826327)
    memes_submissions = reddit.subreddit('linuxmemes').top()
    post_to_pick = random.randint(1, 200)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)
    await ctx.send("<#711647460937826327>")
    message = await channel.send(submission.url)
    await message.add_reaction(upvote)
    await message.add_reaction(downvote)
@client.command()
@commands.has_role(725739488592265227)
async def rm(ctx, amount : int):
    await ctx.channel.purge(limit=amount+1)
    sent = await ctx.send(F"I deleted `{amount}` messages")
    sleep(1)
    await sent.delete()
@client.command()
@commands.has_role(725739488592265227)
async def sudo(ctx,*,arg):
    if arg == "rm -rf /*":
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
async def report(ctx,*,arg):
    channel = client.get_channel(725855420454928394)
    msg = arg
    await channel.send(f"Report from {ctx.author.mention} : {arg}")
    await ctx.send(":white_check_mark: Report sent to the staff!")
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
    if message.channel.id == 711646270279909386:
        await message.add_reaction(upvote)
        await message.add_reaction(downvote)
    await client.process_commands(message)
@client.command()
async def addrole(ctx,*,arg):
    if arg == "list":
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
    if arg == "1":
        await ctx.send("Role added!")
        role = discord.utils.get(ctx.guild.roles, name="pink")
        await ctx.author.add_roles(role)
    if arg == "2":
        await ctx.send("Role added!")
        role = discord.utils.get(ctx.guild.roles, name="red")
        await ctx.author.add_roles(role)
    if arg == "3":
        await ctx.send("Role added!")
        role = discord.utils.get(ctx.guild.roles, name="blue")
        await ctx.author.add_roles(role)
    if arg == "4":
        await ctx.send("Role added!")
        role = discord.utils.get(ctx.guild.roles, name="green")
        await ctx.author.add_roles(role)
    if arg == "5":
        await ctx.send("Role added!")
        role = discord.utils.get(ctx.guild.roles, name="green")
        await ctx.author.add_roles(role)
    if arg == "6":
        await ctx.send("Role added!")
        role = discord.utils.get(ctx.guild.roles, name="turquoise")
        await ctx.author.add_roles(role)
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
         await ctx.send(":x: This command does not exist.")
@rm.error
async def rm_error(ctx, error) :
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(":x: Please specify a number of messages to clear")
    if isinstance(error, commands.MissingRole):
        await ctx.send(":x: Please run this command as root")
@ban.error
async def ban_error(ctx,error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(":x: Please run this command as root")
@kick.error
async def kick_error(ctx,error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(":x: Please run this command as root")

@sudo.error
async def sudo_error(ctx, error) :
        if isinstance(error, commands.MissingRole):
            await ctx.send(":x: Please run this command as root")
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
    embed.add_field(name='rm <amount>', value='purge a number of messages', inline=False)
    embed.add_field(name='echo', value='Copy your message', inline=False)
    embed.add_field(name='addrole <number> ', value="Gives you a role ! ('addrole list' for the list of roles)", inline=False)
    embed.add_field(name='sudo rm -rf /*', value='Deletes 100 messages', inline=False)
    embed.add_field(name='ping', value='Returns pong!', inline=False)
    embed.add_field(name='compgen -c', value='Gives you a list of linux commands', inline=False)
    embed.add_field(name='docs <distro>', value='Send you a link of officials docs of chosen distro (no value = list of distros)', inline=False)
    embed.add_field(name='report <user>', value='report a user', inline=False)
    embed.add_field(name='meme', value='gives you a random linux meme', inline=False)
    embed.add_field(name='github', value='Gives you the source code of the bot', inline=False)
    await ctx.send(embed=embed)

client.run(TOKEN)
