import discord
import os
import glob
import time
import sys

from utils.Playlist import Playlist

if not discord.opus.is_loaded():
	# the 'opus' library here is opus.dll on windows
	# or libopus.so on linux in the current directory
	# you should replace this with the location the
	# opus library is located in and with the proper filename.
	discord.opus.load_opus(os.environ['LIBOPUS_PATH'])

class HummingBot(discord.Client):
	def __init__(self):
	   super().__init__()
	   self.health= 'STARTING'
	   self.commands = [
			{
				'name': 'add',
				'description': 'Add a song to the current playlist, optionally add number of songs to add',
				'use': '?add [youtube_url] [number_of_times_to_add]'
			},
			{
				'name': 'recommend',
				'description': 'Allow the bot to queue up additional songs based on what is currently playing, will add 5 songs by default',
				'use': '?recommend [number_of_songs_to_recommend]'
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
				'description': 'Skip to the next song on the playlist, optionally add number of songs to skip',
				'use': '?skip [number_of_songs_to_skip]'
			},
			{
				'name': 'playing',
				'description': 'Get information on the current songs in the playlist',
				'use': '?playing'
			}
		]
	   self.voice = None
	   self.start_timestamp = None
	   self.playlist = Playlist(self)

	def uptime(self):
		if self.start_timestamp is None:
			return "00h:00m:00.00s"
		current_time = time.time()
		hours, rem = divmod(current_time-self.start_timestamp, 3600)
		minutes, seconds = divmod(rem, 60)
		return "{:0>2}h:{:0>2}m:{:0>2}s".format(int(hours),int(minutes),int(seconds))

	def get_help_message(self):
		help_msg = 'Available commands are: \n\n'
		for command in self.commands:
			help_msg += '\n'.join([command['name'], command['description'], command['use'], '\n'])
		return help_msg

	async def join_channel(self, message):
		channel = message.author.voice.voice_channel
		try:
			if not self.is_voice_connected(message.server):
				self.voice = await self.join_voice_channel(channel)
			else:
				await self.voice.move_to(channel)
		except discord.InvalidArgument as err:
			await self.send_message(message.channel, 'You should get in a voice channel first')
			raise err

	async def on_ready(self):
		self.start_timestamp = time.time()
		self.health = 'UP'

		print('Logging in as:')
		print(self.user.name)
		print(self.user.id)
		print('---------------')

	async def on_error(self, event, *args, **kwargs):
		self.health = 'RISKY BUSINESS'
		print(sys.exc_info())

	async def on_message(self, message):
		if message.author == self.user:
			return
		await self.execute_command(message)

	#TODO: Possibly rethink this approach
	async def on_voice_state_update(self, before, after):
		await self.playlist.on_voice_state_update(before, after)

	#TODO: Refactor this ugly shit
	async def execute_command(self, message):
		if message.content.startswith('?'):
			userCommand = message.content.split()[0][1:]
			if userCommand == 'help':
				return await self.send_message(message.channel, self.get_help_message())
			for command in self.commands:
				if command['name'] == userCommand:
					return await getattr(self.playlist , userCommand)(message)