import asyncio
import discord
import youtube_dl
import functools
from urllib.parse import urlparse
from urllib.parse import parse_qs

from .SongEntry import SongEntry

class Playlist:
	def __init__(self, bot):
		self.bot = bot
		self.songs = asyncio.Queue()
		self.play_next_song = asyncio.Event()
		self.current_song = None

	def get_commands(self):
		commands = [
			{
				'name': 'add',
				'description': 'Add a song to the current playlist',
				'use': '?playlist add [youtube_url]'
			},
			{
				'name': 'pause',
				'description': 'Pause the current song',
				'use': '?playlist pause'	
			},
			{
				'name': 'resume',
				'description': 'Resume the current song',
				'use': '?playlist resume'
			},
			{
				'name': 'clear',
				'description': 'Clear the entire playlist',
				'use': '?playlist clear'
			},
			{
				'name': 'skip',
				'description': 'Skip to the next song on the playlist',
				'use': '?playlist skip'
			},
			{
				'name': 'playing',
				'description': 'Get information on the current songs in the playlist',
				'use': '?playlist playing'
			}
		]
		return commands

	async def add(self, message):
		try:
			await self.bot.join_channel(message)

			# Extract video information, possibly better in the SongEntry class
			#TODO: May need to figure out how to use run_in_executor within SongEntry
			opts = {
				'format': 'webm[abr>0]/bestaudio/best',
				'prefer_ffmpeg': True,
				'noplaylist': True,
				'verbose': True
			}
			with youtube_dl.YoutubeDL(opts) as ydl:
				func = functools.partial(ydl.extract_info, message.content.split()[2], download=False)
				info = await self.bot.loop.run_in_executor(None, func)
				if 'entries' in info:
					info = info['entries'][0]

			new_song = SongEntry(message, message.content.split()[2], info)
			await self.songs.put(new_song)
			await self.bot.add_reaction(message, '🐦')

			print('Added: ' + new_song.title)

			if not self.bot.is_playing() and self.current_song is None:
				await self.play_next()
		except Exception as err:
			print(err)

	async def pause(self, message):
		if message.author.voice_channel is not None:
			self.bot.player.pause()
			await self.bot.add_reaction(message, '🐦')
		else:
			await self.bot.send_message(message.channel, 'You should get in a voice channel first')

	async def skip(self, message):
		if message.author.voice_channel is not None:
			self.bot.player.stop()
			await self.bot.add_reaction(message, '🐦')
		else:
			await self.bot.send_message(message.channel, 'You should get in a voice channel first')

	async def clear(self, message):
		if message.author.voice_channel is not None:
			self.songs = asyncio.Queue()
			self.bot.player.stop()
			await self.bot.add_reaction(message, '🐦')
		else:
			await self.bot.send_message(message.channel, 'You should get in a voice channel first')

	async def resume(self, message):
		if message.author.voice_channel is not None:
			self.bot.player.resume()
			await self.bot.add_reaction(message, '🐦')
		else:
			await self.bot.send_message(message.channel, 'You should get in a voice channel first')

	async def playing(self, message):
		song_list = list(self.songs._queue)

		if (len(song_list) - 2) > 0: await self.bot.send_message(message.channel, 'There are ' + str(len(song_list) - 2) + ' other songs in the queue')

		for song in song_list[1::-1]:
			await self.bot.send_message(message.channel, embed=self.songEmbed(song, 'Coming up'))

		await self.bot.send_message(message.channel, embed=self.songEmbed(self.current_song, 'Now Playing'))

	async def play_next(self):
		while True:
			self.play_next_song.clear()
			self.current_song = None
			try:
				self.current_song = self.songs.get_nowait()
				before_options = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 2'
				self.bot.player = self.bot.voice.create_ffmpeg_player(self.current_song.player_url, before_options=before_options, after=self.finished)
				print('Playing: ' + self.current_song.title)
				self.bot.player.volume = 0.45
				self.bot.player.start()
				await self.play_next_song.wait()
			except:
				return

	def finished(self):
		self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

	def songEmbed(self, song, description):
		#TODO: Have thumbnail logic in SongEntry
		song_embed = discord.Embed(title=song.uploader + ' - ' + song.title, description=description, colour=0xDEADBF)
		youtube_qparams = parse_qs(urlparse(song.url).query)
		if 'v' in youtube_qparams: song_embed.set_thumbnail(url='https://img.youtube.com/vi/%s/0.jpg' % youtube_qparams['v'][0])
		return song_embed
