import tornado.web

from handlers.BaseHandler import BaseHandler

class PlaylistHandler(BaseHandler):
	def initialize(self, bot):
		self.bot = bot

	def get(self):
		songs = []
		current_song = None

		if self.bot.playlist.current_song is not None:
			current_song = self.bot.playlist.current_song.to_rest_dict()
			current_song['timestamp'] = self.bot.playlist.current_song_timer.get_elapsed_seconds()

		for song in list(self.bot.playlist.songs):
			songs.insert(0, song.to_rest_dict())

		self.write({'songs': songs, 'currentSong': current_song})