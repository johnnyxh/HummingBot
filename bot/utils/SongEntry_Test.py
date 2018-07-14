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