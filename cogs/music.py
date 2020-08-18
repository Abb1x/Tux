
from discord.ext import commands
import lavalink
from discord import utils
from discord import Embed


class MusicCog(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.client.music = lavalink.Client(714896470012067922)
    self.client.music.add_node('localhost', 7000, 'testing', 'na', 'music-node')
    self.client.add_listener(self.client.music.voice_update_handler, 'on_socket_response')
    self.client.music.add_event_hook(self.track_hook)

  @commands.command(name='join')
  async def join(self, ctx):
    print('join command worked')
    member = utils.find(lambda m: m.id == ctx.author.id, ctx.guild.members)
    if member is not None and member.voice is not None:
      vc = member.voice.channel
      player = self.client.music.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
      if not player.is_connected:
        player.store('channel', ctx.channel.id)
        await self.connect_to(ctx.guild.id, str(vc.id))
  @commands.command()
  async def stop(self,ctx):
      await ctx.voice_client.disconnect()
  @commands.command()
  async def play(self, ctx, *, query):
    member = utils.find(lambda m: m.id == ctx.author.id, ctx.guild.members)
    if member is not None and member.voice is not None:
      vc = member.voice.channel
      player = self.client.music.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
      if not player.is_connected:
        player.store('channel', ctx.channel.id)
        await self.connect_to(ctx.guild.id, str(vc.id))
    try:
      player = self.client.music.player_manager.get(ctx.guild.id)
      query = f'ytsearch:{query}'
      results = await player.node.get_tracks(query)
      tracks = results['tracks'][0:10]
      i = 0
      query_result = ''
      for track in tracks:
        i = i + 1
        query_result = query_result + f'{i}) {track["info"]["title"]} - {track["info"]["uri"]}\n'
      embed = Embed()
      embed.description = query_result

      await ctx.channel.send(embed=embed)
      await ctx.channel.send("Please choose with the number: ")

      def check(m):
        return m.author.id == ctx.author.id

      response = await self.client.wait_for('message', check=check)
      track = tracks[int(response.content)-1]

      player.add(requester=ctx.author.id, track=track)
      if not player.is_playing:
        await player.play()

    except Exception as error:
      print(error)

  async def track_hook(self, event):
    if isinstance(event, lavalink.events.QueueEndEvent):
      guild_id = int(event.player.guild_id)
      await self.connect_to(guild_id, None)

  async def connect_to(self, guild_id: int, channel_id: str):
    ws = self.client._connection._get_websocket(guild_id)
    await ws.voice_state(str(guild_id), channel_id)

def setup(client):
  client.add_cog(MusicCog(client))
