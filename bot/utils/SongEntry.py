class SongEntry:
	def __init__(self, message, info):
		self.requester = message.author
		self.channel = message.channel
		self.url = info.get('url')
		self.uploader = info.get('uploader')
		self.title = info.get('title')
		self.id = info.get('id')