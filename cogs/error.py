import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
ignore_command_errors = [
    ("help", commands.MissingRequiredArgument),
    ("docs", commands.MissingRequiredArgument)
    ]
class ErrorCog(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener()
    async def on_command_error(self,ctx: commands.Context,error):

        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(description=":x: │ **This command does not exist**",colour=discord.Colour.red())
            return await ctx.send(embed=embed)
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(description=f":x: │ **{ctx.message.author.mention} is not in the sudoers file.This incident will be reported.**",colour=discord.Colour.red())
            return await ctx.send(embed=embed)
        if not (ctx.command.name, type(error)) in ignore_command_errors:
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(description=f":x: │ **Missing required arguments**",colour=discord.Colour.red())
                return await ctx.send(embed=embed)
        if isinstance(error,commands.CommandOnCooldown):
            await ctx.send("Please wait before running this command again!")
def setup(client):
    client.add_cog(ErrorCog(client))
