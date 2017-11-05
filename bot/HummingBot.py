import discord
import os
import glob
import time
import sys

from utils.Playlist import Playlist
from utils.Image import Image

if not discord.opus.is_loaded():
	# the 'opus' library here is opus.dll on windows
	# or libopus.so on linux in the current directory
	# you should replace this with the location the
	# opus library is located in and with the proper filename.
	discord.opus.load_opus(os.environ['LIBOPUS_PATH'])

class HummingBot(discord.Client):
	def __init__(self, sound_directory):
	   super().__init__()
	   self.sound_directory = sound_directory
	   self.health= 'STARTING'
	   self.player = None
	   self.voice = None
	   self.start_timestamp = None
	   self.modules = [Playlist(self), Image(self)]

	def uptime(self):
		if self.start_timestamp is None:
			return "00h:00m:00.00s"
		current_time = time.time()
		hours, rem = divmod(current_time-self.start_timestamp, 3600)
		minutes, seconds = divmod(rem, 60)
		return "{:0>2}h:{:0>2}m:{:0>2}s".format(int(hours),int(minutes),int(seconds))

	def is_playing(self):
		return self.player is not None and self.player.is_playing()

	def show_module_help(self, module):
		help_msg = 'Available commands in the ' + type(module).__name__.lower() + ' module are: \n\n'
		for command in module.get_commands():
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
		try:
			for module in self.modules:
				await getattr(module, 'on_voice_state_update')(before, after)
		except Exception as err:
			print(err)

	#TODO: Refactor this ugly shit
	async def execute_command(self, message):
		if message.content.startswith('?'):
			for module in self.modules:
				if type(module).__name__.lower() == message.content.split()[0][1:]:
					userCommand = message.content.split()[1]
					for command in module.get_commands():
						if command['name'] == userCommand:
							return await getattr(module, userCommand)(message)
					return await self.send_message(message.channel, self.show_module_help(module))
			return await self.play_voice(message, message.content.split()[0][1:])

	async def play_voice(self, message, sound):
		soundname = os.path.join(self.sound_directory, sound)
		filename = glob.glob(soundname + '.*')
		if filename:
			if not self.is_playing():
				try:
					await self.join_channel(message)
					self.player = self.voice.create_ffmpeg_player(filename[0])
					self.player.start();
				except Exception as err:
					print(err)
		else:
			await self.add_reaction(message, '❓')
