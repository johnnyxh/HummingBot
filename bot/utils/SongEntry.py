class SongEntry:
	def __init__(self, message, song_url, info):
		self.requester = message.author
		self.channel = message.channel
		self.url = song_url
		self.uploader = info.get('uploader')
		self.title = info.get('title')
		self.description = info.get('description')
		self.player_url = info['url']
