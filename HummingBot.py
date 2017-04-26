import discord
import argparse
import asyncio
import os.path

from utils.Playlist import Playlist

# Add some command line arguments
parser = argparse.ArgumentParser(description='Starts up the HummingBot.')
parser.add_argument('-t', '--token', dest='token', action='store', help='Your API Bot User token', required=True)
parser.add_argument('-s', '--sounds', dest='soundDirectory', metavar='DIRECTORY', action='store', help='Directory containing sound files for the bot to play', required=False, default='sounds')

args = parser.parse_args()

if not discord.opus.is_loaded():
	# the 'opus' library here is opus.dll on windows
	# or libopus.so on linux in the current directory
	# you should replace this with the location the
	# opus library is located in and with the proper filename.
	discord.opus.load_opus('opus')

class HummingBot(discord.Client):
	def __init__(self, soundDirectory):
		   super().__init__()
		   self.soundDirectory = soundDirectory
		   self.player = None
		   self.voice = None
		   self.modules = [Playlist()]

	def is_playing(self):
		return self.player is not None and self.player.is_playing()

	async def run_command(self, message, userCommand):
		for module in self.modules:
			for command in module.get_commands():
				if command['name'] == userCommand:
					await getattr(module, userCommand)(self, message)


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
		if message.content.startswith('?'):
			await self.run_command(message, message.content.split()[0][1:])
			await self.play_voice(message, message.content.split()[0][1:])

	async def play_voice(self, message, sound):
		if not self.is_playing():
			await self.join_channel(message)
			if os.path.isfile(os.path.join(self.soundDirectory, sound + '.mp3')):
				self.player = self.voice.create_ffmpeg_player(os.path.join(self.soundDirectory, sound + '.mp3'))
				self.player.start();
			elif os.path.isfile(os.path.join(self.soundDirectory, sound + '.wav')):
				self.player = self.voice.create_ffmpeg_player(os.path.join(self.soundDirectory, sound + '.wav'))
				self.player.start();

client = HummingBot(args.soundDirectory)
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(client.start(args.token))
except KeyboardInterrupt:
	print('Logging out...')
	loop.run_until_complete(client.logout())
finally:
    loop.close()
