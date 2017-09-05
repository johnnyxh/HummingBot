import asyncio
import discord
import youtube_dl
import functools
import tempfile
from urllib.parse import urlparse
from urllib.parse import parse_qs

from .SongEntry import SongEntry

class Playlist:
	YOUTUBE_OPTS = {
		'format': 'webm[abr>0]/bestaudio/best',
		'prefer_ffmpeg': True,
		'verbose': True,
	}

	PLAYLIST_DOWNLOAD_RANGE = 5

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
			playlist_count = await self._get_playlist_count(video_url)-1

			if playlist_count >= 0:
				await self.bot.add_reaction(message, '🔄')
				lower_bound = 0
				opts = self.YOUTUBE_OPTS.copy()
				while lower_bound < playlist_count:
					upper_bound = lower_bound + self.PLAYLIST_DOWNLOAD_RANGE
					if upper_bound >= playlist_count: upper_bound = playlist_count
					opts['playlist_items'] = str(lower_bound) + '-' + str(upper_bound)
					info = await self._get_video_info(video_url, opts)
					if 'entries' in info:
						for entry in info['entries']:
							new_song = SongEntry(message, entry)
							await self.songs.put(new_song)
						await self.bot.add_reaction(message, '🐦')
					asyncio.ensure_future(self._play_next())
					lower_bound = upper_bound+1
			else:
				info = await self._get_video_info(video_url, self.YOUTUBE_OPTS)
				new_song = SongEntry(message, info)
				await self.songs.put(new_song)
				await self.bot.add_reaction(message, '🐦')
				await self._play_next()

		except Exception as err:
			print(err)

	async def pause(self, message):
		if await self._user_in_voice_command(message):
			self.bot.player.pause()

	async def skip(self, message):
		if await self._user_in_voice_command(message):
			self.bot.player.stop()

	async def shuffle(self, message):
		#TODO: Get this done
		if await self._user_in_voice_command(message):
			await self.bot.send_message(message.channel, 'Maybe someday')

	async def clear(self, message):
		if await self._user_in_voice_command(message):
			self.songs = asyncio.Queue()
			self.bot.player.stop()

	async def resume(self, message):
		if await self._user_in_voice_command(message):
			self.bot.player.resume()

	async def playing(self, message):
		song_list = list(self.songs._queue)

		if (len(song_list) - 2) > 0: await self.bot.send_message(message.channel, 'There are ' + str(len(song_list) - 2) + ' other songs in the queue')

		for song in song_list[1::-1]:
			await self.bot.send_message(message.channel, embed=song.get_embed_info('Coming up'))

		await self.bot.send_message(message.channel, embed=self.current_song.get_embed_info('Now Playing - %s' % self.current_song.get_current_timestamp()))

	async def on_voice_state_update(self, before, after):
		if self.bot.voice is not None and len(self.bot.voice.channel.voice_members) <= 1:
			self.songs = asyncio.Queue()
			self.bot.player.stop()
			await self.bot.voice.disconnect()

	async def _play_next(self):
		if not self.bot.is_playing() and self.current_song is None:
			while True:
				self.play_next_song.clear()
				self.current_song = None
				try:
					self.current_song = self.songs.get_nowait()
					before_options = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 2'
					self.bot.player = self.bot.voice.create_ffmpeg_player(self.current_song.url, before_options=before_options, after=self._finished)
					print('Playing: ' + self.current_song.title)
					self.bot.player.volume = 0.45
					self.bot.player.start()
					self.current_song.song_started()
					await self.play_next_song.wait()
				except:
					return

	async def _user_in_voice_command(self, message):
		if message.author.voice_channel is not None:
			await self.bot.add_reaction(message, '🐦')
			return True
		else:
			await self.bot.send_message(message.channel, 'You should get in a voice channel first')
			return False

	async def _get_playlist_count(self, youtube_url):
		playlist_count = 0
		youtube_qparams = parse_qs(urlparse(youtube_url).query) 
		if 'list' in youtube_qparams:
			playlist_opts = self.YOUTUBE_OPTS.copy()
			playlist_opts['extract_flat'] = 'in_playlist'
			with youtube_dl.YoutubeDL(playlist_opts) as ydl:
				func = functools.partial(ydl.extract_info, youtube_url, download=False)
				flat_info = await self.bot.loop.run_in_executor(None, func)
				playlist_count = len(flat_info['entries'])
		return playlist_count

	async def _get_video_info(self, youtube_url, opts):
		with youtube_dl.YoutubeDL(opts) as ydl:
			func = functools.partial(ydl.extract_info, youtube_url, download=False)
			return await self.bot.loop.run_in_executor(None, func)

	def _finished(self):
		self.bot.loop.call_soon_threadsafe(self.play_next_song.set)