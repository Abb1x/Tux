import json
import random
import sqlite3

import discord
from discord.ext import commands
import psycopg2
from decouple import config
db_pass = config("DB_PASS")
db_user = config("DB_USER")
db_host = config("DB_HOST")
db_name = config("DB_NAME")

class LevelCog(commands.Cog):
    def __init__(self,client):
        self.client = client

    def add_user_to_db(self, server_id, user_id):
        conn = psycopg2.connect(
            f"dbname={db_name} user={db_user} host={db_host} password={db_pass} options='-c search_path=level'")
        try:
            sql = "INSERT INTO users (server_id,user_id,level,experience) VALUES (%s,%s,0,0)"
            cur = conn.cursor()
            cur.execute(sql, (server_id, user_id))
            conn.commit()
        finally:
            conn.close()
    def add_experience(self,server_id,user_id,experience):
        self.get_exp(server_id,user_id)
        conn = psycopg2.connect(
            f"dbname={db_name} user={db_user} host={db_host} password={db_pass} options='-c search_path=level'")
        try:
            sql = "UPDATE users SET experience = experience + %s WHERE server_id = %s AND user_id = %s;"
            cur = conn.cursor()
            cur.execute(sql, (experience,server_id,user_id))
            conn.commit()
        finally:
            conn.close()
    def id_exists(self,server_id,user_id):
        global user_in
        conn = psycopg2.connect(f"dbname={db_name} user={db_user} host={db_host} password={db_pass} options='-c search_path=level'")
        cur = conn.cursor()
        cur.execute("SELECT EXISTS(SELECT 1 FROM users WHERE server_id = %s AND user_id = %s)", (server_id,user_id))
        if cur.fetchone()[0] == True:
             user_in = True
        else:
             user_in = False
    def get_exp(self,server_id,user_id):
        global exp
        conn = psycopg2.connect(f"dbname={db_name} user={db_user} host={db_host} password={db_pass} options='-c search_path=level'")
        cursor = conn.cursor()
        postgreSQL_select_Query = "select * from users where server_id = %s and user_id = %s"

        cursor.execute(postgreSQL_select_Query, (server_id,user_id))
        money_records = cursor.fetchall()
        for row in money_records:
            exp = row[3]
    def get_lvl(self,server_id,user_id):
        global lvl
        conn = psycopg2.connect(f"dbname={db_name} user={db_user} host={db_host} password={db_pass} options='-c search_path=level'")
        cursor = conn.cursor()
        postgreSQL_select_Query = "select * from users where server_id = %s and user_id = %s"

        cursor.execute(postgreSQL_select_Query, (server_id,user_id))
        money_records = cursor.fetchall()
        for row in money_records:
            lvl = row[2]
    async def level_up(self,user,channel,server_id,user_id):
        global lvl_start
        global lvl_end
        self.get_lvl(server_id,user_id)
        self.get_exp(server_id,user_id)
        lvl_start = lvl
        lvl_end = int(exp ** (1/4))
        if lvl_start < lvl_end:
            await channel.send(f"{user.mention} has leveled up to level {lvl_end}!")
            conn = psycopg2.connect(
                f"dbname={db_name} user={db_user} host={db_host} password={db_pass} options='-c search_path=level'")
            try:
                sql = "UPDATE users SET level = %s WHERE server_id = %s AND user_id = %s;"
                cur = conn.cursor()
                cur.execute(sql, (lvl_end,server_id,user_id))
                conn.commit()
            finally:
                conn.close()
    @commands.command(aliases=['top'])
    async def leaderboard(self,ctx):
        async with ctx.typing():
            if enabled:
                embed=discord.Embed(title=f"Leaderboard of {ctx.guild.name}",color=random.randint(0, 0xffffff))
                embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
                conn = psycopg2.connect(
                    f"dbname={db_name} user={db_user} host={db_host} password={db_pass} options='-c search_path=level'")
                try:
                    sql = "select * from users where server_id = %s ORDER BY level + experience DESC;"
                    cur = conn.cursor()
                    cur.execute(sql,[ctx.guild.id])
                    leaderboard = cur.fetchall()
                    for index,row in enumerate(leaderboard):
                        user = self.client.get_user(row[1])
                        exp = row[3]
                        lvl = row[2]
                        embed.add_field(name=f"{index+1}.{user.name}", value=f"Level: {lvl} XP: {exp}", inline=False)
                    await ctx.send(embed=embed)
                finally:
                    conn.close()
            else:
                await ctx.send("Leveling system is not enabled!")
    @commands.Cog.listener()
    async def on_message(self,message):
        global enabled
        enabled = False
        connection = sqlite3.connect("secondary.db")
        cursor = connection.cursor()
        cursor.execute("select * from Level where server_id = ?", (message.guild.id,))
        records = cursor.fetchall()
        for row in records:
            if row[1] == 1:
                enabled = True
            else:
                enabled = False
        if enabled:
            if not message.author.bot:
                self.id_exists(message.guild.id,message.author.id)
                if user_in == False:
                    self.add_user_to_db(message.guild.id,message.author.id)
                self.add_experience(message.guild.id,message.author.id,5)
                await self.level_up(message.author,message.channel,message.guild.id,message.author.id)
    @commands.command()
    async def rank(self,ctx):
        if enabled:
            async with ctx.typing():
                self.get_exp(ctx.author.id,ctx.guild.id)
                self.get_lvl(ctx.author.id,ctx.guild.id)
                embed = discord.Embed(title=f"Stats of {ctx.author.name}", color=random.randint(0, 0xffffff))
                embed.set_thumbnail(url=f"{ctx.author.avatar_url}")
                embed.add_field(name=f"Level : {lvl}", value=f"\u200b", inline=False)
                embed.add_field(name=f"Experience : {exp}", value=f"\u200b", inline=False)
                await ctx.send(embed=embed)
        else:
            await ctx.send("Leveling system is not enabled!")
    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        conn = psycopg2.connect(f"dbname={db_name} user={db_user} host={db_host} password={db_pass} options='-c search_path=level'")
        cur = conn.cursor()
        cur.execute("DELETE FROM players WHERE server_id = %s;",(guild.id,))
        conn.commit()
        conn.close()
def setup(client):
    client.add_cog(LevelCog(client))