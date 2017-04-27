import asyncio

from .SongEntry import SongEntry

# Right now this isn't much of a playlist, just plays a single video
class Playlist:
	def __init__(self, bot):
		self.bot = bot
		self.songs = asyncio.Queue()
		self.play_next_song = asyncio.Event()
		self.current_song = None
		self.audio_loop = self.bot.loop.create_task(self.play_next())

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

		if not self.bot.is_playing() and self.current_song is None:
			await self.play_next()

	async def pause(self, message):
		self.bot.player.pause()

	async def skip(self, message):
		self.bot.player.stop()

	async def stop(self, message):
		# Do nothing, bring this back at some point
		return

	async def resume(self, message):
		self.bot.player.resume()

	async def playing(self, message):
		# Do nothing, bring this back at some point
		return

	async def play_next(self):
		while True:
			self.play_next_song.clear()
			self.current_song = self.songs.get_nowait()
			before_options = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 2'
			self.bot.player = await self.bot.voice.create_ytdl_player(self.current_song.song, before_options=before_options, after=self.finished)
			self.bot.player.volume = 0.45
			self.bot.player.start()
			await self.play_next_song.wait()

	def finished(self):
		self.bot.loop.call_soon_threadsafe(self.play_next_song.set)
