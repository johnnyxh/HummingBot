class SongEntry:
	def __init__(self, message, song):
		self.requester = message.author
		self.channel = message.channel
		self.song = song
