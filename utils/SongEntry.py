# import youtube_dl

class SongEntry:
	def __init__(self, message, song):
		self.requester = message.author
		self.channel = message.channel
		self.song = song

		#  with youtube_dl.YoutubeDL() as ydl:
		# 	 self.info = ydl.extract_info(song, download=False)
