import unittest
from unittest.mock import patch, MagicMock

from utils.SongEntry import SongEntry

class SongEntryTest(unittest.TestCase):

	def setUp(self):
		self.author = 'SomeGuy'

		self.info_mock = {
			'url': 'http://www.somevideourl.com',
			'title': 'SomeTitle',
			'id': 'pj5huCuhD_Q',
			'uploader': 'SomeUploader'
		}

		self.embed_mock = MagicMock()

	@patch('utils.SongEntry.time')
	def test_song_started_sets_start_timestamp(self, time_mock):
		time_mock.time.return_value = 12345;
		song = SongEntry(self.author, self.info_mock)
		song.song_started()

		self.assertEqual(song.play_start, 12345)

	@patch('utils.SongEntry.time')
	def test_get_current_timestamp_produces_timestamp(self, time_mock):
		time_mock.time.return_value = 20768;
		song = SongEntry(self.author, self.info_mock)
		song.play_start = 10200

		self.assertEqual(song.get_current_timestamp(), '02:56:08.00')

	@patch('utils.SongEntry.discord')
	def test_get_embed_info(self, discord_mock):
		discord_mock.Embed.return_value = self.embed_mock
		description = 'Now Playing'
		song = SongEntry(self.author, self.info_mock)
		song.get_embed_info(description)

		self.assertEqual(discord_mock.Embed.call_args, (({'colour': 0xDEADBF, 'description': description, 'title': self.info_mock['title']}),))
		self.assertEqual(self.embed_mock.set_thumbnail.call_args, (({'url': 'https://img.youtube.com/vi/pj5huCuhD_Q/0.jpg'}),))


if __name__ == '__main__':
	unittest.main()