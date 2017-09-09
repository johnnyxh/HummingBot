import asyncio
import unittest
from unittest.mock import patch, MagicMock

from utils.Playlist import Playlist

class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)

class PlaylistTest(unittest.TestCase):

	def setUp(self):
		self.bot_mock = MagicMock()
		self.message_mock = MagicMock()
		self.song_queue_mock = MagicMock()
		self.message_mock.author.voice_channel

	@patch.object(Playlist, '_user_in_voice_command', new_callable=AsyncMock)
	def test_pause(self, user_in_voice_mock):
		playlist = Playlist(self.bot_mock)
		user_in_voice_mock.return_value = True

		loop = asyncio.get_event_loop()
		loop.run_until_complete(playlist.pause(self.message_mock))

		self.assertTrue(self.bot_mock.player.pause.called)

	@patch.object(Playlist, '_user_in_voice_command', new_callable=AsyncMock)
	def test_pause_not_in_channel(self, user_in_voice_mock):
		playlist = Playlist(self.bot_mock)
		user_in_voice_mock.return_value = False

		loop = asyncio.get_event_loop()
		loop.run_until_complete(playlist.pause(self.message_mock))

		self.assertFalse(self.bot_mock.player.pause.called)

	@patch.object(Playlist, '_user_in_voice_command', new_callable=AsyncMock)
	def test_skip(self, user_in_voice_mock):
		playlist = Playlist(self.bot_mock)
		user_in_voice_mock.return_value = True

		loop = asyncio.get_event_loop()
		loop.run_until_complete(playlist.skip(self.message_mock))

		self.assertTrue(self.bot_mock.player.stop.called)

	@patch.object(Playlist, '_user_in_voice_command', new_callable=AsyncMock)
	def test_skip_not_in_channel(self, user_in_voice_mock):
		playlist = Playlist(self.bot_mock)
		user_in_voice_mock.return_value = False

		loop = asyncio.get_event_loop()
		loop.run_until_complete(playlist.skip(self.message_mock))

		self.assertFalse(self.bot_mock.player.stop.called)

	@patch.object(Playlist, '_user_in_voice_command', new_callable=AsyncMock)
	@patch('utils.Playlist.asyncio')
	def test_clear(self, asyncio_mock, user_in_voice_mock):
		playlist = Playlist(self.bot_mock)
		user_in_voice_mock.return_value = True

		loop = asyncio.get_event_loop()
		loop.run_until_complete(playlist.clear(self.message_mock))

		self.assertTrue(self.bot_mock.player.stop.called)
		self.assertEqual(asyncio_mock.Queue.call_count, 2)

	@patch.object(Playlist, '_user_in_voice_command', new_callable=AsyncMock)
	@patch('utils.Playlist.asyncio')
	def test_clear_not_in_channel(self, asyncio_mock, user_in_voice_mock):
		playlist = Playlist(self.bot_mock)
		user_in_voice_mock.return_value = False

		loop = asyncio.get_event_loop()
		loop.run_until_complete(playlist.clear(self.message_mock))

		self.assertFalse(self.bot_mock.player.stop.called)
		self.assertEqual(asyncio_mock.Queue.call_count, 1)

	@patch.object(Playlist, '_user_in_voice_command', new_callable=AsyncMock)
	def test_resume(self, user_in_voice_mock):
		playlist = Playlist(self.bot_mock)
		user_in_voice_mock.return_value = True

		loop = asyncio.get_event_loop()
		loop.run_until_complete(playlist.resume(self.message_mock))

		self.assertTrue(self.bot_mock.player.resume.called)

	@patch.object(Playlist, '_user_in_voice_command', new_callable=AsyncMock)
	def test_resume_not_in_channel(self, user_in_voice_mock):
		playlist = Playlist(self.bot_mock)
		user_in_voice_mock.return_value = False

		loop = asyncio.get_event_loop()
		loop.run_until_complete(playlist.resume(self.message_mock))

		self.assertFalse(self.bot_mock.player.resume.called)

	@patch('utils.Playlist.asyncio')
	def test_playing_empty_queue(self, asyncio_mock):
		asyncio_mock.Queue._songs = []
		self.message_mock.channel = 'SomeChannel'
		self.bot_mock.send_message = AsyncMock()
		playlist = Playlist(self.bot_mock)

		loop = asyncio.get_event_loop()
		loop.run_until_complete(playlist.playing(self.message_mock))

		self.assertEqual(self.bot_mock.send_message.call_args, (('SomeChannel', 'There are no songs in the queue'),))

	@patch('utils.Playlist.SongEntry')
	@patch('utils.Playlist.asyncio')
	def test_playing_empty_queue_song_playing(self, asyncio_mock, song_entry_mock):
		asyncio_mock.Queue._songs = []
		self.message_mock.channel = 'SomeChannel'
		self.bot_mock.send_message = AsyncMock()
		playlist = Playlist(self.bot_mock)

		song_embed_mock = {'title': 'fakeTitle', 'description': 'some fake description'}
		song_entry_mock.get_embed_info.return_value = song_embed_mock
		playlist.current_song = song_entry_mock

		loop = asyncio.get_event_loop()
		loop.run_until_complete(playlist.playing(self.message_mock))

		args, kwargs = self.bot_mock.send_message.call_args
		self.assertEqual(args, ('SomeChannel',))
		self.assertEqual(kwargs, ({'embed': song_embed_mock}),)

	@patch('utils.Playlist.asyncio')
	def test_playing_two_queue_song_playing(self, asyncio_mock):
		song1 = MagicMock()
		song_embed_mock1 = {'title': 'fakeTitle', 'description': 'some fake description'}
		song1.get_embed_info.return_value = song_embed_mock1

		song2 = MagicMock()
		song_embed_mock2 = {'title': 'someOtherTitle', 'description': 'more fake descriptions'}
		song2.get_embed_info.return_value = song_embed_mock2

		song3 = MagicMock()
		song_embed_mock3 = {'title': 'oneMoreTitle', 'description': 'the last fake description'}
		song3.get_embed_info.return_value = song_embed_mock3

		song_queue = MagicMock()
		song_queue._queue = [song2, song3]
		asyncio_mock.Queue.return_value = song_queue
		self.message_mock.channel = 'SomeChannel'
		self.bot_mock.send_message = AsyncMock()
		playlist = Playlist(self.bot_mock)
		playlist.current_song = song1

		loop = asyncio.get_event_loop()
		loop.run_until_complete(playlist.playing(self.message_mock))

		self.assertEqual(self.bot_mock.send_message.call_count, 3)

		args, kwargs = self.bot_mock.send_message.call_args_list[2]
		self.assertEqual(args, ('SomeChannel',))
		self.assertEqual(kwargs, ({'embed': song_embed_mock1}),)

		args, kwargs = self.bot_mock.send_message.call_args_list[1]
		self.assertEqual(args, ('SomeChannel',))
		self.assertEqual(kwargs, ({'embed': song_embed_mock2}),)

		args, kwargs = self.bot_mock.send_message.call_args_list[0]
		self.assertEqual(args, ('SomeChannel',))
		self.assertEqual(kwargs, ({'embed': song_embed_mock3}),)

	@patch('utils.Playlist.asyncio')
	def test_playing_four_queue_song_playing(self, asyncio_mock):
		song1 = MagicMock()
		song_embed_mock1 = {'title': 'fakeTitle', 'description': 'some fake description'}
		song1.get_embed_info.return_value = song_embed_mock1

		song2 = MagicMock()
		song_embed_mock2 = {'title': 'someOtherTitle', 'description': 'more fake descriptions'}
		song2.get_embed_info.return_value = song_embed_mock2

		song3 = MagicMock()
		song_embed_mock3 = {'title': 'oneMoreTitle', 'description': 'the last fake description'}
		song3.get_embed_info.return_value = song_embed_mock3

		song_queue = MagicMock()
		song_queue._queue = [song2, song3, song3, song3, song3]
		asyncio_mock.Queue.return_value = song_queue
		self.message_mock.channel = 'SomeChannel'
		self.bot_mock.send_message = AsyncMock()
		playlist = Playlist(self.bot_mock)
		playlist.current_song = song1

		loop = asyncio.get_event_loop()
		loop.run_until_complete(playlist.playing(self.message_mock))

		self.assertEqual(self.bot_mock.send_message.call_count, 4)

		args, kwargs = self.bot_mock.send_message.call_args_list[3]
		self.assertEqual(args, ('SomeChannel',))
		self.assertEqual(kwargs, ({'embed': song_embed_mock1}),)

		args, kwargs = self.bot_mock.send_message.call_args_list[2]
		self.assertEqual(args, ('SomeChannel',))
		self.assertEqual(kwargs, ({'embed': song_embed_mock2}),)

		args, kwargs = self.bot_mock.send_message.call_args_list[1]
		self.assertEqual(args, ('SomeChannel',))
		self.assertEqual(kwargs, ({'embed': song_embed_mock3}),)

		args, kwargs = self.bot_mock.send_message.call_args_list[0]
		self.assertEqual(args, ('SomeChannel', 'There are 3 other songs in the queue',))

if __name__ == '__main__':
	unittest.main()