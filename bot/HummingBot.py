import asyncio
import argparse
import discord
import os
import threading
import glob

from utils.Playlist import Playlist
from flask import Flask

# Add some command line arguments
parser = argparse.ArgumentParser(description='Starts up the HummingBot.')
parser.add_argument('-t', '--token', dest='token', action='store', help='Your API Bot User token', required=False)
parser.add_argument('-s', '--sounds', dest='sound_directory', metavar='DIRECTORY', action='store', help='Directory containing sound files for the bot to play', required=False, default='sounds')
parser.add_argument('-o', '--opus', dest='opus_directory', action='store', help='Directory containing the libopus library', required=False)

args = parser.parse_known_args()[0]

if not discord.opus.is_loaded():
	# the 'opus' library here is opus.dll on windows
	# or libopus.so on linux in the current directory
	# you should replace this with the location the
	# opus library is located in and with the proper filename.
	discord.opus.load_opus(args.opus_directory or os.environ['LIBOPUS_PATH'])

class HummingBot(discord.Client):
	def __init__(self, sound_directory):
		   super().__init__()
		   self.sound_directory = sound_directory
		   self.player = None
		   self.voice = None
		   self.modules = [Playlist(self)]

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
		print('Logging in as:')
		print(self.user.name)
		print(self.user.id)
		print('---------------')

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

app = Flask(__name__, static_folder='./static', static_url_path='')

@app.route("/")
def index():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

def start_bot(loop):
	asyncio.set_event_loop(loop)
	client = HummingBot(args.sound_directory)
	try:
	    loop.run_until_complete(client.start(args.token or os.environ['HUMMINGBOT_TOKEN']))
	except KeyboardInterrupt:
		print('Logging out...')
		loop.run_until_complete(client.logout())
	finally:
		loop.close()

loop = asyncio.get_event_loop()
bot_thread = threading.Thread(target=start_bot,args=(loop,))
bot_thread.start()