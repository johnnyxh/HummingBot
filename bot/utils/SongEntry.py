import discord
import time
import math

class SongEntry:
	def __init__(self, requester, info):
		self.requester = requester.display_name
		self.url = info.get('url')
		self.uploader = info.get('uploader')
		self.title = info.get('title')
		self.id = info.get('id')
		self.duration = info.get('duration')
		self.is_live = info.get('is_live')
		self.play_start = 0

	def song_started(self):
		self.play_start = math.floor(time.time())

	def get_current_timestamp(self):
		current_time = math.floor(time.time())
		hours, rem = divmod(current_time-self.play_start, 3600)
		minutes, seconds = divmod(rem, 60)
		return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)

	def get_embed_info(self, description):
		song_embed = discord.Embed(title=self.title, description=description, colour=0xDEADBF)
		song_embed.set_thumbnail(url='https://img.youtube.com/vi/%s/0.jpg' % self.id)
		return song_embed

	def to_rest_dict(self):
		return {'videoId': self.id, 'uploader': self.uploader, 'title': self.title, 'requester': self.requester, 'duration': self.duration, 'timestamp': math.floor(time.time())-self.play_start, 'isLive': self.is_live}