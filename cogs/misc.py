import asyncio
import os
import pathlib

import aiohttp
import discord
from discord.ext import commands
import random
from googletrans import Translator
import wikipedia
import urbandictionary as ud
import requests #used to send get request
import psycopg2
import praw
from decouple import config

import datetime
#api key for weather api
#api key for weather
reddit_secret = config("REDDIT_SECRET")
reddit = praw.Reddit(client_id="c2EFf196cE7pXQ",
                     client_secret=reddit_secret,
                     user_agent='Ububot')
api_key = config("WEATHER_KEY")
base_url = "http://api.openweathermap.org/data/2.5/weather?"
upvote = "<:upvote:726140828090761217>"
downvote = '<:downvote:726140881060757505>'
remove_bg_api_key=config("REMOVEBG_KEY")
start = datetime.datetime.now().replace(microsecond=0)
#Cog for misc commands
class MiscCog(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.command()
    async def github(self, ctx):
        await ctx.send("https://github.com/Abb1x/Tux")
    @commands.command()
    async def echo(self, ctx, *, arg):
        await ctx.send(f"{arg}")

    @commands.command()
    async def ping(self,ctx):
        await ctx.send(f':ping_pong: Pong **{round(self.client.latency * 1000)}ms**')

    @commands.command()
    async def skin(self,ctx,arg):
        embed=discord.Embed(title=f"{arg}'s minecraft skin")
        embed.set_image(url=f"https://mc-heads.net/avatar/{arg}/500/")
        await ctx.send(embed=embed)

    @commands.command(aliases=["8ball","ball"])
    async def _8ball(self,ctx,arg):
        responses = ["It is certain.",

                    "It is decidedly so.",

                    "Without a doubt.",

                    "Yes - definitely.",

                    "You may rely on it.",

                    "As I see it, yes.",

                    "Most likely.",

                    "Outlook good.",

                    "Yes.",

                    "Signs point to yes.",

                    "Reply hazy, try again.",

                    "Ask again later.",

                    "Better not tell you now.",

                    "Cannot predict now.",

                    "Concentrate and ask again.",

                    "Don't count on it.",

                    "My reply is no.",

                    "My sources say no.",

                    "Outlook not so good.",

                    "Very doubtful."
    ]

        await ctx.send(random.choice(responses))

    @commands.command()
    async def avatar(self,ctx,member: discord.Member):
        embed=discord.Embed(title=f"{member.name}'s avatar")
        embed.set_image(url=f"{member.avatar_url}")
        await ctx.send(embed=embed)
    @commands.command()
    async def trans(self,ctx,arg,arg2):
        translator = Translator()
        translation = translator.translate(f'{arg}',dest=f"{arg2}")
        embed=discord.Embed(title="Translator", color=0x4f8bed)
        embed.add_field(name="Original Word:", value=f"`{translation.origin}`", inline=False)
        embed.add_field(name="Translated Word:", value=f"`{translation.text}`", inline=True)
        await ctx.send(embed=embed)
    @commands.command(aliases=['wikipedia','pedia'])
    async def wiki(self,ctx,*,arg):
        search = wikipedia.search(f"{arg}")
        result = search[0]
        page = wikipedia.page(f"{result}",auto_suggest=False)
        wiki = wikipedia.summary(f"{result}",sentences=1,auto_suggest=False)
        images = page.images
        rand = random.randint(1,20)
        embed=discord.Embed(title="Wikipedia", colour=0xf4eded)
        embed.add_field(name="Search", value=f"`{arg}`", inline=False)
        embed.add_field(name="Result", value=f"`{wiki}`", inline=True)
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/1200px-Wikipedia-logo-v2.svg.png")
        await ctx.send(embed=embed)
    @commands.command()
    async def weather(self,ctx,*,arg):
        complete_url = base_url + "appid=" + api_key + "&q=" + arg
        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            z = x["sys"]
            current_temperature = y["temp"]

            w = x["weather"]

            basic = w[0]

            sky = basic["description"]

            country = z["country"]

            current_pressure = y["pressure"]

            current_humidiy = y["humidity"]

            z = x["weather"]

            lower_country = country.lower()
            weather_description = z[0]["description"]
            celsius = round(current_temperature-273.15,3)
            embed=discord.Embed(title="Weather",color=discord.Colour.from_rgb(255, 255, 8))
            embed.add_field(name=f":cityscape: City: {arg}", value="\u200b", inline=False)
            embed.add_field(name=f":flag_{lower_country}: Country: {country}", value="\u200b", inline=True)
            embed.add_field(name=f":thermometer: Temperature: {celsius} °C", value="\u200b", inline=False)
            embed.add_field(name=f":droplet: Humidity: {current_humidiy}%", value="\u200b", inline=True)
            embed.add_field(name=f":white_sun_cloud: Sky: {sky}", value="\u200b", inline=False)

            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f":x: │ **City not found**",colour=discord.Colour.red())
            await ctx.send(embed=embed)
    @commands.command()
    async def urban(self,ctx,*,arg):
        defs = ud.define(f'{arg}')
        d = defs[0]
        def_final = d.definition.translate({ord(i): None for i in '[]'})
        embed=discord.Embed(color=0xdf3908)
        embed.set_author(name="Urban Dictionary",icon_url="https://i.pinimg.com/originals/37/46/41/374641157f9fa2ae904664d6c89b984b.jpg")
        embed.add_field(name="Search", value=f"`{arg}`", inline=False)
        embed.set_thumbnail(url="https://i.pinimg.com/originals/37/46/41/374641157f9fa2ae904664d6c89b984b.jpg")
        embed.add_field(name="Result", value=f"`{def_final}`", inline=True)
        await ctx.send(embed=embed)
    @commands.command()
    async def joke(self,ctx):
        data = requests.get("https://official-joke-api.appspot.com/random_joke")
        rand_joke = data.json()
        str = rand_joke
        embed=discord.Embed(title="Random joke",color=random.randint(0,0xffffff))
        embed.add_field(name=f"Category: {str['type']}", value="\u200b", inline=False)
        embed.add_field(name=f"Joke: {str['setup']}", value=f"{str['punchline']}", inline=True)
        await ctx.send(embed=embed)
    @commands.command(aliases=['dmeme','memes'])
    async def dankmeme(self,ctx):
        try:
            async with ctx.typing():
                memes_submissions = reddit.subreddit('memes').hot()
                post_to_pick = random.randint(1,100)
                for i in range(0, post_to_pick):
                    submission = next(x for x in memes_submissions if not x.stickied)
                    embed=discord.Embed(title=f"{submission.title}",url=f"{submission.url}",color=random.randint(0, 0xffffff))
                    embed.set_author(name="r/memes")
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
        except:
            await ctx.send("Sorry, an error occurred please retry")
    @commands.command()
    async def choose(self,ctx,*,choices):
        choices = choices.split(" ")
        choice = random.choice(choices).strip()
        embed=discord.Embed(title="Choose command", color=random.randint(0, 0xffffff))
        embed.add_field(name="Choices:", value=f"`{choices}`", inline=False)
        embed.add_field(name="Choice:", value=f"`{choice}`", inline=True)
        await ctx.send(embed=embed)
    @commands.command()
    async def twans(self,ctx,*,arg):
        def replaceMultiple(mainString, toBeReplaces, newString):
            for elem in toBeReplaces :
                if elem in mainString :
                    # Replace the string
                    mainString = mainString.replace(elem, newString)

            return mainString
        trans = replaceMultiple(arg, ['l', 'r'] , "w")
        await ctx.send(trans)
    @commands.command()
    async def ngskin(self,ctx,arg):
            embed=discord.Embed(title=f"{arg}'s nationsglory skin")
            embed.set_image(url=f"https://skins.nationsglory.fr/face/{arg}/64")
            await ctx.send(embed=embed)
    @commands.command()
    async def info(self,ctx):
        global start
        end = datetime.datetime.now().replace(microsecond=0)
        uptime = end - start
        embed=discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name="Tux v0.5",icon_url="https://images-ext-1.discordapp.net/external/o0qmGA7HWp5CLR0_qdh4ISSemzj4JIQivBJxVbFChwM/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/725734772479098880/b266fa6609aab9d47d65a6f9687f09ba.webp?width=549&height=549")
        embed.add_field(name=f"Ping: {round(self.client.latency * 1000)}ms", value="\u200b", inline=False)
        embed.add_field(name=f"Library: Discord.py 1.3.4 ", value="\u200b", inline=False)
        embed.add_field(name=f"Servers: {len(self.client.guilds)} ", value="\u200b", inline=False)
        embed.add_field(name=f"Uptime: {uptime}",value="\u200b", inline=False)
        embed.add_field(name=f"Created by: <:abbix:738920766451482714> Abbix#4319", value="\u200b", inline=False)
        await ctx.send(embed=embed)
    @commands.command()
    async def removebg(self,ctx,*,arg):
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            data={
                'image_url': f'{arg}',
                'size': 'auto'
            },
            headers={'X-Api-Key': f'{remove_bg_api_key}'},
        )
        if response.status_code == requests.codes.ok:
            with open('no-bg.png', 'wb') as out:
                out.write(response.content)
                await ctx.send("**Image with removed background:**",file=discord.File('no-bg.png'))
                os.remove('no-bg.png')
        else:
            await ctx.send("An error occurred")
    @commands.command(aliases=['rps'])
    async def rockpaperscissors(self,ctx,move):
        choices = ["Rock","Paper","Scissors"]
        choice = random.choice(choices)
        if choice == "Rock" and move == "scissors":
            await ctx.send(f"I choose **{choice}**, I won!")
        if choice == "Paper" and move == "rock":
            await ctx.send(f"I choose **{choice}**, I won!")
        if choice == "Scissors" and move == "paper":
            await ctx.send(f"I choose **{choice}**, I won!")
        if choice.lower() == move:
            await ctx.send(f"I choose **{choice}**, Nobody won :(")
        if choice == "Paper" and move == "scissors":
            await ctx.send(f"I choose **{choice}**, You won!")
        if choice == "Scissors" and move == "rock":
            await ctx.send(f"I choose **{choice}**, You won!")
        if choice == "Rock" and move == "paper":
            await ctx.send(f"I choose **{choice}**, You won!")
    @commands.command()
    async def cowsay(self,ctx,*,arg):
        await ctx.send(f"""**{ctx.author.name}**: 
``` 
< {arg} >
        \   ^__^
         \  (oo)\_______
            (__)\       )\/
                ||----w |
                ||     ||  ```""")

def setup(client):
    client.add_cog(MiscCog(client))
