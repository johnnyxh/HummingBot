import asyncio
import async_timeout
import youtube_dl
import functools
from collections import deque
from urllib.parse import urlparse
from urllib.parse import parse_qs

from utils.SongEntry import SongEntry
from utils.Timer import Timer

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
		self.current_song_timer = None

	async def add(self, message):
		try:
			await self.bot.join_channel(message)

			args = message.content.split()

			video_url = args[1]
			add_count = 1
			
			if len(args) > 2:
				add_count = int(args[2])

			playlist_count = await self._get_playlist_count(video_url)-1

			## Remove the use of _get_video_info here
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
								# Temporary workaround for playlist case, this logic should move
								new_song = SongEntry(message.author, message.channel, entry.get('url'))
								await new_song.create(entry)
								self.songs.appendleft(new_song)
						await self.bot.add_reaction(message, '🐦')
					asyncio.ensure_future(self._play_next())
					lower_bound = upper_bound+1
			else:
				new_song = SongEntry(message.author, message.channel, video_url)
				await new_song.create()
				for songs in range(add_count):
					self.songs.appendleft(new_song)
				await self.bot.add_reaction(message, '🐦')
				await self._play_next()

		except Exception as err:
			raise(err)

	async def recommend(self, message):
		if await self._user_in_voice_command(message):
			recommend_count = 5

			if self.current_song is None:
				return await self.bot.send_message(message.channel, 'You need to play something first')

			args = message.content.split()
			if len(args) > 1:
				recommend_count = int(args[1])

			recommendations = await self.current_song.get_recommendations(self.bot.user, recommend_count)

			self.songs.extendleft(recommendations)

	async def skip(self, message):
		if await self._user_in_voice_command(message):

			try:
				args = message.content.split()
				if len(args) > 1:
					for x in range(int(args[1])-1):
						self.songs.pop()
			except IndexError as err:
				pass
			finally:
				if self.player is not None: self.player.stop()

	async def pause(self, message):
		if await self._user_in_voice_command(message):
			if self.player is not None and self.player.is_playing():
				self.player.pause()
				self.current_song_timer.pause()

	async def resume(self, message):
		if await self._user_in_voice_command(message):
			if self.player is not None and not self.player.is_playing(): 
				self.player.resume()
				self.current_song_timer.resume()

	async def clear(self, message):
		if await self._user_in_voice_command(message):
			if self.player is not None:
				self.songs.clear()
				self.player.stop()

	async def playing(self, message):
		song_list = list(self.songs)

		if len(song_list) <= 0 and self.current_song is None: return await self.bot.send_message(message.channel, 'There are no songs in the queue')

		if (len(song_list) - self.PLAYLIST_PLAYING_RANGE) > 0: await self.bot.send_message(message.channel, 'There are ' + str(len(song_list) - self.PLAYLIST_PLAYING_RANGE) + ' other songs in the queue')

		for song in song_list[len(song_list)-self.PLAYLIST_PLAYING_RANGE:]:
			await self.bot.send_message(message.channel, embed=song.get_embed_info('Coming up'))

		return await self.bot.send_message(message.channel, embed=self.current_song.get_embed_info('Now Playing - {}'.format(self.current_song_timer.get_current_timestamp())))

	async def on_voice_state_update(self, before, after):
		if self.bot.voice is not None and len(self.bot.voice.channel.voice_members) <= 1:
			self.songs.clear()
			self.player.stop()
			await self.bot.voice.disconnect()

	def is_playing(self):
		return self.player is not None and self.player.is_playing()

	async def _play_next(self):
		if not self.is_playing() and self.current_song is None:
			while True:
				self.play_next_song.clear()
				self.current_song = None
				try:
					self.current_song = self.songs.pop()
					before_options = '-ss {} -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 2'.format(self.current_song.start_time)
					self.player = self.bot.voice.create_ffmpeg_player(self.current_song.url, before_options=before_options, after=self._finished)
					self.player.start()
					self.current_song_timer = Timer()
					self.current_song_timer.start()
					print('Playing: {}'.format(self.current_song.title))
					await self.bot.send_message(self.current_song.request_channel, embed=self.current_song.get_embed_info('Now Playing')) 
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

	def _finished(self):
		self.bot.loop.call_soon_threadsafe(self.play_next_song.set)