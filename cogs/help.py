import discord
from discord.ext import commands
class HelpCog(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.command()
    async def help(self,ctx,arg):
        author = ctx.message.author
        await author.create_dm()
        embed = discord.Embed(
        title = "Commands",
        color=0x1df314
        )
        if arg == "moderation":
            embed.add_field(name='`>ban [member] (optional reason)`', value='Bans a member', inline=False)
            embed.add_field(name='`>unban [member]`', value='Unbans a member', inline=False)
            embed.add_field(name='`>kick [member]`', value='Kicks a member', inline=False)
            embed.add_field(name='`>mute [member]`', value='Mutes a member (beta)', inline=False)
            embed.add_field(name='`>rm [amount]`', value='Purge a number of messages', inline=False)
            embed.add_field(name='`>sudo rm -rf /*`', value='Deletes 100 messages', inline=False)
            embed.add_field(name='`>user-info [member]`',value="Gives you info about a member",inline=False)
            embed.add_field(name='`>server-info`',value="Gives you info about the current server",inline=False)
            embed.add_field(name='`>antispam [on/off]`',value="Turn the antispam off or on (experimental)",inline=False)
            embed.add_field(name='`>unmute [member]`',value="Unmute someone",inline=False)
        if arg == "linux":
                embed.add_field(name='`>compgen -c`', value='Gives you a list of linux commands', inline=False)
                embed.add_field(name='`>docs [distro]`', value='Send you a link of officials docs of chosen distro (no value = list of distros)', inline=False)
                embed.add_field(name='`>meme`', value='gives you a random linux meme (beta)', inline=False)
                embed.add_field(name='`>package [pacman/apt][name]`', value='Search a package in the debian or arch repos', inline=False)
                embed.add_field(name='`>ask [question]`', value='Search a question on askubuntu', inline=False)
                embed.add_field(name='`>license`', value='Gives you the license of the bot', inline=False)
        if arg == "misc":
            embed.add_field(name='`>echo`', value='Copies your message', inline=False)
            embed.add_field(name='`>ping`', value='Returns pong!', inline=False)
            embed.add_field(name='`>skin [Player name]`', value='Gives you the minecraft skin depending on the nickname', inline=False)
            embed.add_field(name='`>8ball [question]`', value='Play 8ball', inline=False)
            embed.add_field(name='`>avatar [member]`', value='Gives you the profile picture of chosen user', inline=False)
            embed.add_field(name='`>github`', value='Gives you the source code of the bot', inline=False)
            embed.add_field(name='`>trans [word to translate] [language(French=fr)]`', value='Translate a word to chosen language(words needs to be quoted)', inline=False)
            embed.add_field(name='`>wikipedia [search]`',value="Search a word on Wikipedia")
            embed.add_field(name='`>weather [city]`',value="Gives the current weather in a city",inline=False)
            embed.add_field(name="`>urban [search]`",value="Search on the urban dictionary",inline=False)
            embed.add_field(name="`>joke`",value="Gives you a random joke",inline=False)
            embed.add_field(name="`>choose [choice 1] [choice 2] [...]`",value="Choose between arguments given",inline=False)
            embed.add_field(name="`>twans [sentence]`",value="Translate to owo language",inline=False)
            embed.add_field(name="`>info`",value="Sends you info about the bot",inline=False)
        await ctx.send(embed=embed)
    @help.error
    async def help_error(self,ctx,error):
        if isinstance(error, commands.MissingRequiredArgument):
                embed=discord.Embed(color=0x1df314)
                embed.set_author(name="Tux's commands", icon_url="https://images-ext-1.discordapp.net/external/o0qmGA7HWp5CLR0_qdh4ISSemzj4JIQivBJxVbFChwM/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/725734772479098880/b266fa6609aab9d47d65a6f9687f09ba.webp?width=549&height=549")
                embed.add_field(name="Moderation", value="`>help moderation`", inline=True)
                embed.add_field(name="Linux", value="`>help linux`", inline=True)
                embed.add_field(name="Misc", value="`>help misc`", inline=True)
                embed.add_field(name="\u200b",value="[Invite Me!](https://discord.com/api/oauth2/authorize?client_id=725734772479098880&permissions=8&scope=bot)")
                embed.add_field(name="\u200b",value="[Support server](https://discord.gg/fX9gtQh)",inline=True)
                await ctx.send(embed=embed)
def setup(client):
    client.add_cog(HelpCog(client))