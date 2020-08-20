#!/usr/bin/env python3
import os
import sys
import time
import psycopg2
import discord
from discord.ext import commands
from decouple import config
from discord.ext.commands import has_permissions

print(f"Discord.py Version: {discord.__version__}")
cd_mapping = commands.CooldownMapping.from_cooldown(12, 20, commands.BucketType.member)
spamming = 0
antispam = False
server_in = False
showcase_channel_id = 1
upvote = "<:upvote:726140828090761217>"
downvote = '<:downvote:726140881060757505>'

# Bot Administrators: USE THIS TO CONFIGURE BOT FOR HOSTING
token = config('TOKEN') # Get this from https://discord.com/developers/applications/
# Don't share this information with anyone. Requires a PostgreSQL server.
db_pass = config("DB_PASS") # Yes, plain text. Your users won't be able to see this.
db_user = config("DB_USER") # Using the 'root' user isn't recommended. Use another unique account if possible.
db_host = config("DB_HOST") # Host of the computer serving the database. May look like 'db.example.com', or 'localhost'
db_name = config("DB_NAME") # The name of the database, the name which you place as an argument to the 'USE' command when interacting through a CLI to the db.

#----------------------Header------------------------
client = commands.Bot(command_prefix = '!')
client.remove_command('help')

#----------------------Commands----------------------
def get_channel_id(server_id):
    global showcase_channel_id
    conn = psycopg2.connect("dbname=db_name user=db_user host=db_host password=db_pass options='-c search_path=showcase_channel'")
    cursor = conn.cursor()
    postgreSQL_select_Query = "SELECT * FROM servers WHERE server_id = %s"

    cursor.execute(postgreSQL_select_Query, (server_id,))
    channels_records = cursor.fetchall()
    for row in channels_records:
        showcase_channel_id = row[1]
@client.command()
async def antispam(ctx,arg):
    global antispam
    if arg == "on":
        antispam = True
        await ctx.send("Antispam is turned **on** !")
    if arg == "off":
        antispam = False
        await ctx.send("Antispam is turned **off** !")
# The commands in this section should, at some point, be moved to the appropriate cog.
@client.event
async def on_message(message): # Controls Antispam
    global cd_mapping
    # Controls Showcase Functions

    get_channel_id(message.guild.id)
    global spamming
    global antispam
    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = False
    overwrite.read_messages = True
    retry_after = cd_mapping.update_rate_limit(message)
    role = discord.utils.get(message.guild.roles, name="Muted")
    if antispam == True:
        if not message.author.bot:
            if not message.author.guild_permissions.administrator:
                if type(retry_after) is float:

                    spamming += 1
                    if spamming < 3:
                        await message.channel.send(f"{message.author.mention} **Stop Spamming!**")
                        if spamming > 3:
                            spamming = 0
                        if spamming == 3:
                            if discord.utils.get(message.guild.roles, name="Muted"):
                                await message.author.add_roles(role)
                                spamming = 0
                            else:
                                created_role = await message.guild.create_role(name='Muted', permissions=discord.Permissions(0))
                                for channel in message.guild.channels:
                                    await channel.set_permissions(created_role, overwrite=overwrite)
                                    await message.author.add_roles(created_role)
                                    await message.channel.send(f"{message.author.mention} **Enjoy your mute!**")
    if message.content.startswith(('How you doin','How you doing','how you doin','how you doing')):
        await message.channel.send("https://tenor.com/view/joey-mattle-blanc-friends-how-you-doin-gif-8921348")
    if message.content.startswith(('Hey','Hello','Hi','hello','hi','hey')):
        await message.add_reaction("👋")
    # Controls Showcase Functions
    if message.attachments:
        if message.attachments[0].width is not None:
            if message.channel.id == int(showcase_channel_id):
                await message.add_reaction(upvote)
                await message.add_reaction(downvote)

    await client.process_commands(message)
@client.command()
async def docs(ctx,*,arg):
    distros = {
    "Ubuntu": "https://docs.ubuntu.com/",
    "Arch": "https://wiki.archlinux.org/",
    "Gentoo": "https://wiki.gentoo.org/wiki/Main_Page",
    "Fedora": "https://docs.fedoraproject.org/en-US/docs/",
    "Debian": "https://www.debian.org/doc/",
    "Manjaro": "https://wiki.manjaro.org",
    "OpenSUSE": "https://doc.opensuse.org/",
    "Kali": "https://www.kali.org/docs/",
    "Zorin": "https://zorinos.com/",
    "Mint": "https://linuxmint.com/documentation.php",
    "Venom": "https://osdn.net/projects/venomlinux/wiki/FrontPage",
    "Elementary": "https://elementary.io/docs",
    "Clear": "https://docs.clearos.com/en",
    "Sparky": "https://wiki.sparkylinux.org/doku.php"
    }
    distro = distros[arg]
    if arg in distros:
        await ctx.send(f"Here are the Official Docs for {arg}: {distro}")
        
#----------------------Cogs--------------------------
extensions = [ # list of cogs to load
    "moderation",
    "misc",
    "linux",
    #"error",
    "help",
    "economy",
    "welcome"
]
#loading cogs
if __name__ == "__main__":
    print("\nLoading cogs:")
    for extension in extensions:
        client.load_extension(f"cogs.{extension}")
        print(f"\tLoaded {extension}")
    print("")
    
#----------------------Error Handling-------------------------

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
            embed.add_field(name='Arch',value = "arch",inline=False)
            embed.add_field(name='Fedora',value = "fedora",inline=False)
            embed.add_field(name='Gentoo',value = "gentoo",inline=False)
            embed.add_field(name='Zorin',value = "zorin",inline=False)
            embed.add_field(name="Manjaro",value="manjaro",inline=False)
            embed.add_field(name="openSUSE",value="opensuse",inline=False)
            embed.add_field(name="Kali",value="kali",inline=False)
            embed.add_field(name="Mint",value="mint",inline=False)
            embed.add_field(name="Venom",value="venom",inline=False)
            embed.add_field(name="ElementaryOS",value="elementary",inline=False)
            embed.add_field(name="ClearOS",value="clear",inline=False)
            embed.add_field(name="Sparky",value="sparky",inline=False)
            await ctx.send(embed=embed)

ignore_command_errors = [ # ignore these commands when there's an error
    ("help", commands.MissingRequiredArgument),
    ("docs", commands.MissingRequiredArgument)
    ]
# Database stuff
# TODO Change to a cog?
def add_server_to_db(server_id,channel_id):
    conn = psycopg2.connect("dbname=db_name user=db_user host=db_host password=db_pass options='-c search_path=showcase_channel'")
    try:
        sql = "INSERT INTO servers (server_id,channel_id) VALUES (%s,%s)"
        cur = conn.cursor()
        cur.execute(sql,(server_id,channel_id))
        conn.commit()
    finally:
        conn.close()
def id_exists(server_id):
    global server_in
    conn = psycopg2.connect("dbname=db_name user=db_user host=db_host password=db_pass options='-c search_path=showcase_channel'")
    cur = conn.cursor()
    cur.execute("SELECT EXISTS(SELECT 1 FROM servers WHERE server_id = %s)", (server_id,))
    if cur.fetchone()[0] == True:
        server_in = True
    else:
        server_in=False
def update_data(ch_id,serv_id):
    conn = psycopg2.connect("dbname=db_name user=db_user host=db_host password=db_pass options='-c search_path=showcase_channel'")
    cur = conn.cursor()
    cur.execute("UPDATE servers SET channel_id = %s WHERE server_id = %s;" % (ch_id,serv_id))
    conn.commit()
    conn.close()

@client.command()
@has_permissions(manage_messages=True)
async def showcase(ctx,arg):
    id_exists(ctx.guild.id)
    id = arg.translate({ord(i): None for i in '<#>'})
    try:
        if server_in == False:
            add_server_to_db(ctx.guild.id,id)
            print("Server added to the list")
            await ctx.send(f"Showcase channel set to {arg}!")
        else:
            update_data(id,ctx.guild.id)
            print("Data updated")
    except Exception:
        await ctx.send("Please enter a valid channel!")
@client.command()
@has_permissions(manage_messages=True)
async def rm_showcase(ctx):
    conn = psycopg2.connect("dbname=db_name user=db_user host=db_host password=db_pass options='-c search_path=showcase_channel'")
    cur = conn.cursor()
    cur.execute("DELETE FROM servers WHERE server_id = %s;",(ctx.guild.id,))
    conn.commit()
    conn.close()
    showcase_channel_id = 0
    await ctx.send("Showcase Reversed!")
    
#----------------------Start-------------------------
@client.event
async def on_connect():
    print("Connected. Readying...")
@client.event
async def on_ready():
    iter_length = len(list(client.get_all_members()))
    await client.change_presence(status=discord.Status.online, activity=discord.Game(f">help | {len(client.guilds)} servers & {iter_length} users"))
    print('Bot Online')
@client.event
async def on_guild_join(guild):
    iter_length = len(list(client.get_all_members()))
    await client.change_presence(status=discord.Status.online, activity=discord.Game(f">help | {len(client.guilds)} servers & {iter_length} users"))

@client.event
async def on_disconnect():
    print("Disconnected.\a")
    
#----------------------Footer------------------------
client.run(token)
