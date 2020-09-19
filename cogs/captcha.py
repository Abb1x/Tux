import os
import sqlite3
import time

import discord
import string
from PIL import ImageFont, ImageDraw, Image
import numpy as np
img = np.zeros(shape=(25, 60, 3), dtype=np.uint8)
import random
from discord.ext import commands
import cv2

class CaptchaCog(commands.Cog):
    def __init__(self,client):
        self.client = client
    @commands.command()
    async def verify(self,ctx):
        size = random.randint(10, 16)
        length = random.randint(4, 8)
        img = np.zeros(((size * 2) + 5, length * size, 3), np.uint8)
        img_pil = Image.fromarray(img + 255)

        # Drawing text and lines
        font = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf', size)
        draw = ImageDraw.Draw(img_pil)
        text = ''.join(
            random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)
            for _ in range(length))
        draw.text((5, 10), text, font=font,
                  fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        draw.line([(random.choice(range(length * size)), random.choice(range((size * 2) + 5)))
                      , (random.choice(range(length * size)), random.choice(range((size * 2) + 5)))]
                  , width=1, fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

        # Adding noise and blur
        img = np.array(img_pil)
        thresh = random.randint(1, 5) / 100
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                rdn = random.random()
                if rdn < thresh:
                    img[i][j] = random.randint(0, 123)
                elif rdn > 1 - thresh:
                    img[i][j] = random.randint(123, 255)
        img = cv2.blur(img, (int(size / random.randint(5, 10)), int(size / random.randint(5, 10))))

        # Displaying image
        scale_percent = 320  # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        resize = cv2.resize(src=img,dsize=dim, interpolation = cv2.INTER_AREA)
        cv2.imwrite(f"captcha-resized-{text}.png", resize)
        await ctx.send(file=discord.File(f"captcha-resized-{text}.png"))
        os.remove(f"captcha-resized-{text}.png")
        msg = await self.client.wait_for('message', timeout=60)
        if str(msg.content) == text:
            embed = discord.Embed(title="Correct :white_check_mark: !",color=random.randint(0, 0xffffff))
            embed.add_field(name=f"Verified",value=f"{ctx.author.mention} is now verified")
            sent = await ctx.send(embed=embed)
            role = discord.utils.get(ctx.guild.roles, name="captcha")
            await msg.author.remove_roles(role)
            time.sleep(3)
            amount = 40
            await ctx.channel.purge(limit=amount)
        elif str(msg.content) is not text and str(msg.content) is not "!verify" or str(msg.content) is not ">verify":
            await ctx.send(":x: Wrong letters, please run `>verify`")
    @commands.Cog.listener()
    async def on_member_join(self,member):
        global enabled
        enabled = False
        connection = sqlite3.connect("secondary.db")
        cursor = connection.cursor()
        cursor.execute("select * from captcha where server_id = ?", (member.guild.id,))
        records = cursor.fetchall()
        for row in records:
            if row[1] == 1:
                enabled = True
                id_channel = self.client.get_channel(row[2])
            else:
                enabled = False
        if enabled:
            role = discord.utils.get(member.guild.roles, name="captcha")
            overwrite = discord.PermissionOverwrite()
            overwrite.send_messages = False
            overwrite.read_messages = False
            overwrites = discord.PermissionOverwrite()
            overwrites.send_messages = True
            overwrites.read_messages = True
            if discord.utils.get(member.guild.roles, name="captcha"):
                await member.add_roles(role)
            else:
                role = await member.guild.create_role(name='captcha', permissions=discord.Permissions(0))
                await member.add_roles(role)

                for channel in member.guild.channels:
                    if channel.id != id_channel.id:
                        await channel.set_permissions(role, overwrite=overwrite)
                await id_channel.set_permissions(role, overwrite=overwrites)

        await id_channel.send(f"**Welcome {member.mention}!** verify yourself with `>verify`")
    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        conn = sqlite3.connect("secondary.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM captcha WHERE server_id = %s;",(guild.id,))
        conn.commit()
        conn.close()
def setup(client):
    client.add_cog(CaptchaCog(client))