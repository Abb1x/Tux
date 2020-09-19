import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from decouple import config
import random
import psycopg2
money = 0
crime_amount = 0
work_amount = 0
mine_amount = 0
db_pass = config("DB_PASS")
db_user = config("DB_USER")
db_host = config("DB_HOST")
db_name = config("DB_NAME")
class EconomyCog(commands.Cog):
    def __init__(self,client):
        self.client = client
    def add_user_to_db(self,server_id,user_id):
        player_id = f"{user_id}"
        conn = psycopg2.connect(f"dbname={db_name} user={db_user} host={db_host} password={db_pass} options='-c search_path=economy'")
        try:
            sql = "INSERT INTO players (server_id,user_id,money) VALUES (%s,%s,0)"
            cur = conn.cursor()
            cur.execute(sql,(server_id,player_id))
            conn.commit()
        finally:
            conn.close()
    def get_money(self,server_id,user_id):
        global money
        conn = psycopg2.connect(f"dbname={db_name} user={db_user} host={db_host} password={db_pass} options='-c search_path=economy'")
        cursor = conn.cursor()
        postgreSQL_select_Query = "select * from players where server_id = %s and user_id = %s"

        cursor.execute(postgreSQL_select_Query, (server_id,user_id))
        money_records = cursor.fetchall()
        for row in money_records:
            money = row[2]
        return money
    def update_money_crime(self,server_id,user_id):
            self.get_money(server_id,user_id)
            global money
            global crime_amount
            crime_amount = random.randint(-900,700)
            money += crime_amount
            conn = psycopg2.connect(f"dbname={db_name} user={db_user} host={db_host} password={db_pass} options='-c search_path=economy'")
            try:
                sql = "UPDATE players SET money = %s WHERE server_id = %s AND user_id = %s" % (money,server_id,user_id)
                cur = conn.cursor()
                cur.execute(sql,(server_id,user_id))
                conn.commit()
            finally:
                conn.close()
    def update_money_work(self,server_id,user_id):
            self.get_money(server_id,user_id)
            global money
            global work_amount
            work_amount = random.randint(0,500)
            money += work_amount
            conn = psycopg2.connect(f"dbname={db_name} user={db_user} host={db_host} password={db_pass} options='-c search_path=economy'")
            try:
                sql = "UPDATE players SET money = %s WHERE server_id = %s AND user_id = %s" % (money,server_id,user_id)
                cur = conn.cursor()
                cur.execute(sql,(server_id,user_id))
                conn.commit()
            finally:
                conn.close()
    def update_money_mine(self,server_id,user_id):
            self.get_money(server_id,user_id)
            global money
            global mine_amount

            mine_amount = random.randint(-500,500)
            money += mine_amount
            conn = psycopg2.connect(f"dbname={db_name} user={db_user} host={db_host} password={db_pass} options='-c search_path=economy'")
            try:
                sql = "UPDATE players SET money = %s WHERE server_id = %s AND user_id = %s" % (money,server_id,user_id)
                cur = conn.cursor()
                cur.execute(sql,(server_id,user_id))
                conn.commit()
            finally:
                conn.close()
    def check_user_db(self,server_id,user_id):
        conn = psycopg2.connect(f"dbname={db_name} user={db_user} host={db_host} password={db_pass} options='-c search_path=economy'")
        cur = conn.cursor()
        cur.execute("SELECT EXISTS(SELECT 1 FROM players WHERE server_id = %s AND user_id = %s)", (server_id,user_id))
        return cur.fetchone()[0]
    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.member)
    async def work(self,ctx):
        work_answers =  [
        "You worked as a barista and earned : %s $",
        "You worked as a game developer and earned : %s $",
        "You earned: %s $ while streaming",
        "You lost a teeth,the tooth fairy gave you : %s $",
        "You managed to sold your birthday present, you earned : %s $"
        ]
        player_id = ctx.author.id
        if not self.check_user_db(ctx.guild.id,player_id):
            self.add_user_to_db(ctx.guild.id,player_id)
            #add user to db if he's not already there
        self.update_money_work(ctx.guild.id,player_id)
        embed=discord.Embed(title=random.choice(work_answers) % work_amount,color=discord.Colour.green())
        await ctx.send(embed=embed)
    @commands.command(aliases=['bal','purse'])
    async def balance(self,ctx):
        if self.get_money(ctx.guild.id,ctx.author.id):
            await ctx.send(f"You currently have : **{money} $**")
        else:
            await ctx.send("You don't have any money!")
    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.member)
    async def crime(self,ctx):
        player_id = ctx.author.id
        if not self.check_user_db(ctx.guild.id,player_id):
            self.add_user_to_db(ctx.guild.id,player_id)
        self.update_money_crime(ctx.guild.id,ctx.author.id)
        if crime_amount > 0:
            crime_good_answers = [
            "You robbed a bank and got %s $",
            "You stole and sold your grandfather's car, you got %s $",
            "You mugged someone and got %s $",
            "You were hired as bounty hunter and got %s $"
]
            embed=discord.Embed(title=random.choice(crime_good_answers) % crime_amount,color=discord.Colour.green())
            await ctx.send(embed=embed)
        else:
            crime_bad_answers = [
            "A police caught you stealing a sandwich, you got fined %s $ and lost your sandwich.",
            "You were caught making a graffiti, you were fined %s $",
            "You were caught eating all free samples in a grocery store, pay a fine of %s $",
            "You were caught stealing a lollipop from a kid pay a fine of %s $"
            ]
            embed=discord.Embed(title=random.choice(crime_bad_answers) % crime_amount,color=discord.Colour.red())
            await ctx.send(embed=embed)
    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.member)
    async def mine(self,ctx):
        player_id = ctx.author.id
        if not self.check_user_db(ctx.guild.id,player_id):
            self.add_user_to_db(ctx.guild.id,player_id)
        self.update_money_mine(ctx.guild.id,player_id)
        if mine_amount > 0:
            await ctx.send(f"You got : {mine_amount} $ !")
        else:
            await ctx.send(f"You lost : {mine_amount} $ !")

    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        conn = psycopg2.connect(f"dbname={db_name} user={db_user} host={db_host} password={db_pass} options='-c search_path=economy'")
        cur = conn.cursor()
        cur.execute("DELETE FROM players WHERE server_id = %s;",(guild.id,))
        conn.commit()
        conn.close()
def setup(client):
    client.add_cog(EconomyCog(client))
