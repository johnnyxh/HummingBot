import discord
import time

class SongEntry:
	def __init__(self, message, info):
		self.requester = message.author
		self.channel = message.channel
		self.url = info.get('url')
		self.uploader = info.get('uploader')
		self.title = info.get('title')
		self.id = info.get('id')
		self.play_start = 0

	def song_started(self):
		self.play_start = time.time()

	def get_current_timestamp(self):
		current_time = time.time()
		hours, rem = divmod(current_time-self.play_start, 3600)
		minutes, seconds = divmod(rem, 60)
		return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)

	def get_embed_info(self, description):
		song_embed = discord.Embed(title=self.title, description=description, colour=0xDEADBF)
		song_embed.set_thumbnail(url='https://img.youtube.com/vi/%s/0.jpg' % self.id)
		return song_embed