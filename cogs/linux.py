import discord
from discord.ext import commands
import praw
import random
import requests
import asyncio
import json
import os
from bs4 import BeautifulSoup
from decouple import config
reddit_secret = config("REDDIT_SECRET")
from datetime import datetime
reddit = praw.Reddit(client_id="c2EFf196cE7pXQ",
                     client_secret=reddit_secret,
                     user_agent='Ububot')
upvote = "<:upvote:726140828090761217>"
downvote = '<:downvote:726140881060757505>'
class LinuxCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def license(self, ctx): # would like this to be a subcommand of license at some point.
        embed=discord.Embed(title="MIT License", description="  A short and simple permissive license with conditions only requiring preservation of copyright and license notices. Licensed works, modifications, and larger works may be distributed under different terms and without source code.")
        embed.set_thumbnail(url="https://duckduckgo.com/i/07eb45d6.png")
        embed.add_field(name="Permissions", value="✅ Commercial use\n✅ Modification\n✅ Distribution\n✅ Private use", inline=True)
        embed.add_field(name="Limitations", value="❌ Liability\n❌ Warranty", inline=True)
        embed.add_field(name="Conditions", value="ℹ License and copyright notice", inline=True)
        embed.set_footer(text="This is not legal advice. ")
        await ctx.send(embed=embed)
    @commands.command(aliases=['compgen -c','comp'])
    #might remove this command
    async def compgen(self,ctx):
        await ctx.send("https://fossbytes.com/a-z-list-linux-command-line-reference/")
    @commands.command()
    async def meme(self,ctx):
        async with ctx.typing():
            memes_submissions = reddit.subreddit('linuxmemes').hot()
            post_to_pick = random.randint(1,100)
            for i in range(0, post_to_pick):
                submission = next(x for x in memes_submissions if not x.stickied)
                embed=discord.Embed(title=f"{submission.title}",url=f"{submission.url}",color=random.randint(0, 0xffffff))
                embed.set_author(name="r/linuxmemes")
                embed.set_image(url=f"{submission.url}")
        message = await ctx.send(embed=embed)
        await message.add_reaction(upvote)
        await message.add_reaction(downvote)
        await message.add_reaction("🗑️")
        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) == '🗑️'

        try:
            await self.client.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            pass
        else:
            await message.delete()
    @commands.command(aliases=['pkg'])
    async def package(self,ctx,arg,arg2):
        if arg == "apt":
            pkg_url = "https://sources.debian.org/api/src/" + arg2 + "/"
            pkg = requests.get(pkg_url)
            f = pkg.json()
            if not "error" in f:
                name = f["package"]
                version = f["versions"][0]["version"]
                embed=discord.Embed(title=f"{arg2}",color=0xd70751,description=f"sudo apt install {arg2}")
                embed.add_field(name="Version:",value=f"{version}")
                message = await ctx.send(embed=embed)
                await message.add_reaction("🗑️")

                def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) == '🗑️'

                try:
                    await self.client.wait_for('reaction_add', timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    pass
                else:
                    await message.delete()
            else:
                srch_url = "https://sources.debian.org/api/search/" + arg2 + "/"
                srch = requests.get(srch_url)
                j = srch.json()
                other = j["results"]["other"]
                one = other[0]["name"]
                embed = discord.Embed(title=f"Package Not found",colour=discord.Colour.red(),description="Did you mean:")
                embed.add_field(name=f"{one}",value="From debian package list")
                await ctx.send(embed=embed)
        if arg == "pacman":
            pkg_url = "https://www.archlinux.org/packages/search/json/?q=" + arg2
            pkg = requests.get(pkg_url)
            f = pkg.json()
            if ["results"][0] in f:
                repo = f["results"][0]["repo"]
                version = f["results"][0]["pkgver"]
                desc = f["results"][0]["pkgdesc"]
                link = f["results"][0]["url"]
                embed=discord.Embed(title=f"{arg2}",color=0x4aabdb,description=f"sudo pacman -S {arg2}")
                embed.add_field(name="Repo:",value=f"{repo}",inline=False)
                embed.add_field(name="Version:",value=f"{version}",inline=False)
                embed.add_field(name="Description:",value=f"{desc}",inline=False)
                embed.add_field(name="Link:",value=f"{link}",inline=False)
                message = await ctx.send(embed=embed)
                await message.add_reaction("🗑️")

                def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) == '🗑️'

                try:
                    await self.client.wait_for('reaction_add', timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    pass
                else:
                    await message.delete()
            if not ["results"][1] in f:
                embed = discord.Embed(title=f"Package Not found",colour=discord.Colour.red())
                await ctx.send(embed=embed)
    @commands.command()
    async def ask(self,ctx,*,arg):
        response = requests.get(f"https://api.stackexchange.com/2.2/search?order=desc&sort=activity&intitle={arg}&site=askubuntu")
        data = response.json()
        if data["has_more"]:
            title = data["items"][0]["title"]
            tags = data["items"][0]["tags"]
            owner_name = data["items"][0]["owner"]["display_name"]
            owner_image = data["items"][0]["owner"]["profile_image"]
            link = data["items"][0]["link"]
            creation_date = data["items"][0]["creation_date"]
            answers = data["items"][0]["answer_count"]
            views = data["items"][0]["view_count"]
            score = data["items"][0]["score"]
            embed=discord.Embed(title=title,url=f"{link}",description=f"created at: {datetime.utcfromtimestamp(creation_date).strftime('%Y-%m-%d %H:%M:%S')}",color=0xec6f22)
            embed.set_author(name=f"{owner_name}",icon_url=f"{owner_image}")
            embed.set_thumbnail(url="https://cdn.cybrhome.com/media/website/live/icon/icon_askubuntu.com_520990.png")
            embed.add_field(name="Link:", value=f"{link}", inline=False)
            embed.add_field(name="Answers:", value=f"{answers}", inline=False)
            embed.add_field(name="Views:", value=f"{views}", inline=False)
            embed.add_field(name="Score:", value=f"{score}", inline=True)
            tag_name = ', '.join(tags)
            embed.set_footer(text=f"Tags: {tag_name}")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f":x: │ **Question not found**",colour=discord.Colour.red())
            await ctx.send(embed=embed)
        await embed.add_reaction("🗑️")

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) == '🗑️'

        try:
            await self.client.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            pass
        else:
            await embed.delete()
def setup(client):
    client.add_cog(LinuxCog(client))
