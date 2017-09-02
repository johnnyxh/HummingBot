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
				'name': 'shuffle',
				'description': 'Shuffle the order of the playlist',
				'use': '?playlist shuffle'
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

			video_url = message.content.split()[2]

			# Extract video information, possibly better in the SongEntry class
			#TODO: May need to figure out how to use run_in_executor within SongEntry
			opts = {
				'format': 'webm[abr>0]/bestaudio/best',
				'prefer_ffmpeg': True,
				'verbose': True
			}

			youtube_qparams = parse_qs(urlparse(video_url).query) 
			if 'list' in youtube_qparams: 
				await self.bot.send_message(message.channel, 'Adding a youtube playlist to the song queue. This will take some time')
				await self.bot.add_reaction(message, '🔄')

			with youtube_dl.YoutubeDL(opts) as ydl:
				func = functools.partial(ydl.extract_info, video_url, download=False)
				info = await self.bot.loop.run_in_executor(None, func)
				if 'entries' in info:
					for entry in info['entries']:
						new_song = SongEntry(message, entry['url'], entry)
						await self.songs.put(new_song)
					await self.bot.add_reaction(message, '🐦')
				else:
					new_song = SongEntry(message, video_url, info)
					await self.songs.put(new_song)
					print('Added: ' + new_song.title)


			await self.bot.add_reaction(message, '🐦')

			if not self.bot.is_playing() and self.current_song is None:
				await self._play_next()
		except Exception as err:
			print(err)

	async def pause(self, message):
		if self._user_in_voice_command(message.author):
			self.bot.player.pause()

	async def skip(self, message):
		if self._user_in_voice_command(message.author):
			self.bot.player.stop()

	async def shuffle(self, message):
		if self._user_in_voice_command(message.author):
			await self.bot.send_message(message.channel, 'Maybe someday')

	async def clear(self, message):
		if self._user_in_voice_command(message.author):
			self.songs = asyncio.Queue()
			self.bot.player.stop()

	async def resume(self, message):
		if self._user_in_voice_command(message.author):
			self.bot.player.resume()

	async def playing(self, message):
		song_list = list(self.songs._queue)

		if (len(song_list) - 2) > 0: await self.bot.send_message(message.channel, 'There are ' + str(len(song_list) - 2) + ' other songs in the queue')

		for song in song_list[1::-1]:
			await self.bot.send_message(message.channel, embed=self._songEmbed(song, 'Coming up'))

		await self.bot.send_message(message.channel, embed=self._songEmbed(self.current_song, 'Now Playing'))

	async def on_voice_state_update(self, before, after):
		if self.bot.voice is not None and len(self.bot.voice.channel.voice_members) <= 1:
			self.songs = asyncio.Queue()
			self.bot.player.stop()
			await self.bot.voice.disconnect()

	async def _play_next(self):
		while True:
			self.play_next_song.clear()
			self.current_song = None
			try:
				self.current_song = self.songs.get_nowait()
				before_options = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 2'
				self.bot.player = self.bot.voice.create_ffmpeg_player(self.current_song.player_url, before_options=before_options, after=self._finished)
				print('Playing: ' + self.current_song.title)
				self.bot.player.volume = 0.45
				self.bot.player.start()
				await self.play_next_song.wait()
			except:
				return

	async def _user_in_voice_command(self, user):
		if user.voice_channel is not None:
			await self.bot.add_reaction(message, '🐦')
			return True
		else:
			await self.bot.send_message(message.channel, 'You should get in a voice channel first')
			return False

	def _finished(self):
		self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

	def _songEmbed(self, song, description):
		#TODO: Have thumbnail logic in SongEntry
		song_embed = discord.Embed(title=song.uploader + ' - ' + song.title, description=description, colour=0xDEADBF)
		youtube_qparams = parse_qs(urlparse(song.url).query)
		if 'v' in youtube_qparams: song_embed.set_thumbnail(url='https://img.youtube.com/vi/%s/0.jpg' % youtube_qparams['v'][0])
		return song_embed