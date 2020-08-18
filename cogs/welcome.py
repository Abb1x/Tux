import psycopg2
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from decouple import config
server_in = False
db_pass = config("DB_PASS")
db_user = config("DB_USER")
db_host = config("DB_HOST")
db_name = config("DB_NAME")
class WelcomeCog(commands.Cog):
    def __init__(self,client):
        self.client = client

    def get_welcome_message(self,server_id):
        global welcome_msg
        conn = psycopg2.connect(
            "dbname=db_name user=db_user host='db_host' password='db_pass' options='-c search_path=welcome'")
        cursor = conn.cursor()
        postgreSQL_select_Query = "select * from messages where server_id = %s"

        cursor.execute(postgreSQL_select_Query, (server_id,))
        channels_records = cursor.fetchall()
        for row in channels_records:
            welcome_msg = row[1]
    def add_server_to_db(self,server_id, message):
        conn = psycopg2.connect(
            "dbname=db_name user=db_user host='db_host' password='db_pass' options='-c search_path=welcome'")
        try:
            sql = "INSERT INTO messages (server_id,message) VALUES (%s,%s)"
            cur = conn.cursor()
            cur.execute(sql, (server_id, message))
            conn.commit()
        finally:
            conn.close()

    def id_exists(self,server_id):
        global server_in
        conn = psycopg2.connect(
              "dbname=db_name user=db_user host='db_host' password='db_pass' options='-c search_path=welcome'")
        cur = conn.cursor()
        cur.execute("SELECT EXISTS(SELECT 1 FROM messages WHERE server_id = %s)", (server_id,))
        if cur.fetchone()[0] == True:
             server_in = True
        else:
             server_in = False

    def update_data(self,message,serv_id):
        conn = psycopg2.connect(
            "dbname=db_name user=db_user host='db_host' password='db_pass' options='-c search_path=welcome'")
        cur = conn.cursor()
        cur.execute("UPDATE messages SET message = '%s' WHERE server_id = %s;" % (message, serv_id))
        conn.commit()
        conn.close()
    @commands.command()
    @has_permissions(manage_messages=True)
    async def welcome(self,ctx,*,msg):
            self.id_exists(ctx.guild.id)
            if server_in == False:
                self.add_server_to_db(ctx.guild.id, msg)
                await ctx.send(f"Welcome message set to `{msg}` !")
            else:
                self.update_data(msg,ctx.guild.id)
            await ctx.send(f"Welcome message set to `{msg}` !")
    @commands.command()
    @has_permissions(manage_messages=True)
    async def rm_welcome(self,ctx):
        global welcome_msg
        conn = psycopg2.connect(
            "dbname=db_name user=db_user host='db_host' password='db_pass' options='-c search_path=welcome'")
        cur = conn.cursor()
        cur.execute("DELETE FROM messages WHERE server_id = %s;", (ctx.guild.id,))
        conn.commit()
        conn.close()
        welcome_msg = None
        await ctx.send("Welcome message deleted!")
    @commands.command()
    async def print_msg(self,ctx):
        print(welcome_msg)
    @commands.Cog.listener()
    async def on_member_join(self,member):
        global welcome_msg
        channel = self.client.get_channel(member.guild.system_channel.id)
        self.get_welcome_message(member.guild.id)
        if "{mention}" in welcome_msg:
            formatted_msg = welcome_msg.replace("{mention}",f"{member.mention}")
        if "{server_name}" in welcome_msg:
            formatted_msg = welcome_msg.replace("{server_name}",f"{member.guild.name}")
        if "{server_name}" in welcome_msg and "{mention}" in welcome_msg:
            formatted_msg = welcome_msg.replace("{server_name}", f"{member.guild.name}")
            formatted_msg = formatted_msg.replace("{mention}",f"{member.mention}")
        await channel.send(formatted_msg)
def setup(client):
    client.add_cog(WelcomeCog(client))