import asyncio

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
				'name': 'play',
				'description': 'Add a youtube video to the current playlist'
			},
			{
				'name': 'pause',
				'description': 'Pause the current video'
			},
			{
				'name': 'resume',
				'description': 'Resume the current video'
			},
			{
				'name': 'stop',
				'description': 'Stop the entire playlist'
			},
			{
				'name': 'skip',
				'description': 'Skip to the next video on the playlist'
			},
			{
				'name': 'playing',
				'description': 'Get information on the curent song'
			}
		]
		return commands

	async def play(self, message):
		await self.bot.join_channel(message)
		new_song = SongEntry(message, message.content.split()[1])
		await self.songs.put(new_song)
		await self.bot.add_reaction(message, '🐦')

		print('Added: ' + new_song.song)

		if not self.bot.is_playing() and self.current_song is None:
			await self.play_next()

	async def pause(self, message):
		self.bot.player.pause()

	async def skip(self, message):
		self.bot.player.stop()

	async def stop(self, message):
		self.songs = asyncio.Queue()
		self.bot.player.stop()
		return

	async def resume(self, message):
		self.bot.player.resume()

	async def playing(self, message):
		# Have this list all songs in the queue at some point
		# Use embeds instead of plain text
		await self.bot.send_message(message.channel, 'Currently playing: ' + self.bot.player.uploader + ' - ' + self.bot.player.title)
		return

	async def play_next(self):
		while True:
			self.play_next_song.clear()
			self.current_song = None
			try:
				self.current_song = self.songs.get_nowait()
				before_options = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 2'
				youtube_options = {'noplaylist': True}
				self.bot.player = await self.bot.voice.create_ytdl_player(self.current_song.song, ytdl_options=youtube_options, before_options=before_options, after=self.finished)
				print('Playing: ' + self.current_song.song)
				self.bot.player.volume = 0.45
				self.bot.player.start()
				await self.play_next_song.wait()
			except:
				return

	def finished(self):
		self.bot.loop.call_soon_threadsafe(self.play_next_song.set)
