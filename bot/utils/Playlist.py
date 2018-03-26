import aiohttp
import asyncio
import async_timeout
import youtube_dl
import functools
import os
from collections import deque
from urllib.parse import urlparse
from urllib.parse import parse_qs

from utils.SongEntry import SongEntry

class Playlist:
	YOUTUBE_OPTS = {
		'format': 'webm[abr>0]/bestaudio/best',
		'prefer_ffmpeg': True,
		'verbose': True,
		'playlistrandom': True,
		'ignoreerrors': True
	}

	PLAYLIST_PLAYING_RANGE = 2
	PLAYLIST_DOWNLOAD_RANGE = 5

	def __init__(self, bot):
		self.bot = bot
		self.player = None
		self.songs = deque()
		self.play_next_song = asyncio.Event()
		self.current_song = None
		self.is_autopilot = False

	def get_commands(self):
		commands = [
			{
				'name': 'add',
				'description': 'Add a song to the current playlist',
				'use': '?add [youtube_url]'
			},
			{
				'name': 'autopilot',
				'description': 'Toggle on to have the bot add to the playlist automatically based on what\'s currently playing',
				'use': '?autopilot'
			},
			{
				'name': 'repeat',
				'description': 'Add the current song to the front of queue',
				'use': '?repeat'
			},
			{
				'name': 'pause',
				'description': 'Pause the current song',
				'use': '?pause'	
			},
			{
				'name': 'resume',
				'description': 'Resume the current song',
				'use': '?resume'
			},
			{
				'name': 'clear',
				'description': 'Clear the entire playlist',
				'use': '?clear'
			},
			{
				'name': 'skip',
				'description': 'Skip to the next song on the playlist',
				'use': '?skip'
			},
			{
				'name': 'playing',
				'description': 'Get information on the current songs in the playlist',
				'use': '?playing'
			}
		]
		return commands

	async def add(self, message):
		try:
			await self.bot.join_channel(message)

			video_url = message.content.split()[1]

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
							if entry is not None:
								new_song = SongEntry(message.author, entry)
								self.songs.appendleft(new_song)
						await self.bot.add_reaction(message, '🐦')
					asyncio.ensure_future(self._play_next())
					lower_bound = upper_bound+1
			else:
				info = await self._get_video_info(video_url, self.YOUTUBE_OPTS)
				new_song = SongEntry(message.author, info)
				self.songs.appendleft(new_song)
				await self.bot.add_reaction(message, '🐦')
				await self._play_next()

		except Exception as err:
			raise(err)

	async def autopilot(self, message):
		if await self._user_in_voice_command(message):
			self.is_autopilot = not self.is_autopilot
			await self.bot.send_message(message.channel, 'Playlist autopilot set to: ' + str(self.is_autopilot))

	async def repeat(self, message):
		if await self._user_in_voice_command(message):
			if self.current_song is None: return await self.bot.send_message(message.channel, 'There is no song currently playing')
			self.songs.append(self.current_song)

	async def pause(self, message):
		if await self._user_in_voice_command(message):
			if self.player is not None: self.player.pause()

	async def skip(self, message):
		if await self._user_in_voice_command(message):
			if self.player is not None: self.player.stop()

	async def clear(self, message):
		if await self._user_in_voice_command(message):
			if self.player is not None:
				self.songs.clear()
				self.player.stop()

	async def resume(self, message):
		if await self._user_in_voice_command(message):
			if self.player is not None: self.player.resume()

	async def playing(self, message):
		song_list = list(self.songs)

		if len(song_list) <= 0 and self.current_song is None: return await self.bot.send_message(message.channel, 'There are no songs in the queue')

		if (len(song_list) - self.PLAYLIST_PLAYING_RANGE) > 0: await self.bot.send_message(message.channel, 'There are ' + str(len(song_list) - self.PLAYLIST_PLAYING_RANGE) + ' other songs in the queue')

		for song in song_list[len(song_list)-self.PLAYLIST_PLAYING_RANGE:]:
			await self.bot.send_message(message.channel, embed=song.get_embed_info('Coming up'))

		return await self.bot.send_message(message.channel, embed=self.current_song.get_embed_info('Now Playing - %s' % self.current_song.get_current_timestamp()))

	async def on_voice_state_update(self, before, after):
		if self.bot.voice is not None and len(self.bot.voice.channel.voice_members) <= 1:
			self.is_autopilot = False
			self.songs.clear()
			self.player.stop()
			await self.bot.voice.disconnect()

	def is_playing(self):
		return self.player is not None and self.player.is_playing()

	async def _play_next(self):
		if not self.is_playing() and self.current_song is None:
			while True:
				self.play_next_song.clear()
				await self._run_autopilot()
				self.current_song = None
				try:
					self.current_song = self.songs.pop()
					before_options = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 2'
					self.player = self.bot.voice.create_ffmpeg_player(self.current_song.url, before_options=before_options, after=self._finished)
					print('Playing: ' + self.current_song.title)
					self.player.volume = 0.45
					self.player.start()
					self.current_song.song_started()
					await self.play_next_song.wait()
				except :
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

	async def _run_autopilot(self):
		if self.is_autopilot and len(self.songs) <= 0:
			async with aiohttp.ClientSession() as session:
				with async_timeout.timeout(10):
					async with session.get('https://www.googleapis.com/youtube/v3/search?type=video&relatedToVideoId=' + self.current_song.id + '&part=snippet&key=' + os.environ['YOUTUBE_API_KEY']) as response:
						jsonBody = await response.json()
						info = await self._get_video_info('https://www.youtube.com/watch?v=' + jsonBody['items'][0]['id']['videoId'], self.YOUTUBE_OPTS)
						new_song = SongEntry('bot', info)
						self.songs.appendleft(new_song)

	def _finished(self):
		self.bot.loop.call_soon_threadsafe(self.play_next_song.set)