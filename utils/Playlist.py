import asyncio

from .SongEntry import SongEntry

# Right now this isn't much of a playlist, just plays a single video
class Playlist:
	def __init__(self):
		self.songs = asyncio.Queue()
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
				'name': 'skip',
				'description': 'Skip to the next video on the playlist'
			},
			{
				'name': 'playing',
				'description': 'Get information on the curent song'
			}
		]
		return commands

	async def play(self, bot, message):
		await bot.join_channel(message)
		newSong = SongEntry(message, message.content.split()[1])
		#await self.songs.put(newSong)
		await bot.add_reaction(message, '🐦')

		if not bot.is_playing() and self.current_song is None:
			before_options = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 2'
			bot.player = await bot.voice.create_ytdl_player(newSong.song, before_options=before_options)
			bot.player.start()

	async def pause(self, bot, message):
		# Do nothing, bring this back at some point
		return

	async def skip(self, bot, message):
		bot.player.stop()

	async def playing(self, bot, message):
		# Do nothing, bring this back at some point
		return
