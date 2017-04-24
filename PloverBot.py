import discord
import argparse
import asyncio
import os.path

# Add some command line arguments
parser = argparse.ArgumentParser(description='Starts up the Plover bot.')
parser.add_argument('-t', '--token', dest='token', action='store', help='Your API Bot User token', required=True)

args = parser.parse_args()

if not discord.opus.is_loaded():
	# the 'opus' library here is opus.dll on windows
	# or libopus.so on linux in the current directory
	# you should replace this with the location the
	# opus library is located in and with the proper filename.
	discord.opus.load_opus('opus')

class VoiceEntry:
	def __init__(self, message, song):
		self.requester = message.author
		self.channel = message.channel
		self.song = song

class PloverBot(discord.Client):
	def __init__(self):
		   super().__init__()
		   self.player = None
		   self.voice = None
		   self.commands = []

	def is_playing(self):
		return self.player is not None and self.player.is_playing()

	async def join_channel(self, message):
		channel = message.author.voice.voice_channel
		if not self.is_voice_connected(message.server):
			self.voice = await self.join_voice_channel(channel)
		else:
			await self.voice.move_to(channel)

	async def on_ready(self):
		print('Logging in as:')
		print(self.user.name)
		print(self.user.id)
		print('---------------')

	async def on_message(self, message):
		if message.author == self.user:
			return
		await self.execute_command(message)

	async def execute_command(self, message):
		messageList = message.content.split()
		for i, item in enumerate(messageList):
			if item.startswith('?'):
				await self.play_voice(message, item[1:])

	async def play_voice(self, message, sound):
		if not self.is_playing():
			await self.join_channel(message)
			if os.path.isfile('sounds/' + sound + '.mp3'):
				self.player = self.voice.create_ffmpeg_player('sounds/' + sound + '.mp3')
				self.player.start();
			elif os.path.isfile('sounds/' + sound + '.wav'):
				self.player = self.voice.create_ffmpeg_player('sounds/' + sound + '.wav')
				self.player.start();

client = PloverBot()
client.run(args.token)
