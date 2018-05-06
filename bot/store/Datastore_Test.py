import asyncio
import unittest
from unittest.mock import patch, MagicMock

from store.Datastore import Datastore

class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)

class DatastoreTest(unittest.TestCase):

	@patch('store.Datastore.motor.motor_asyncio')
	def test_initialization_default(self, motor_mock):
		datastore = Datastore()

		args, kwargs = motor_mock.AsyncIOMotorClient.call_args
		self.assertEqual(args, ('mongodb://localhost:27017',))

	@patch('store.Datastore.motor.motor_asyncio')
	def test_initialization_uri(self, motor_mock):
		datastore = Datastore('mongodb://user:password@some.domain:27017/some_db')

		args, kwargs = motor_mock.AsyncIOMotorClient.call_args
		self.assertEqual(args, ('mongodb://user:password@some.domain:27017/some_db',))

	@patch('store.Datastore.motor.motor_asyncio')
	def test_insert_new(self, motor_mock):
		song = MagicMock()

		mock_connection = { 'hummingbot': AsyncMock() }
		motor_mock.AsyncIOMotorClient.return_value = mock_connection

		song.to_rest_dict.return_value = { 'videoId': 'kUaAszRmBbQ', 'title': 'Partner' }
		mock_connection['hummingbot'].songs.find_one_and_update.return_value = None

		datastore = Datastore()
		loop = asyncio.get_event_loop()
		loop.run_until_complete(datastore.insert_song(song, 'piano'))

		args, kwargs = mock_connection['hummingbot'].songs.insert_one.call_args
		self.assertEqual(args, ({ 'videoId': 'kUaAszRmBbQ', 'title': 'Partner', 'play_count': 1, 'skip_count': 0, 'song_label': 'piano' },))

	@patch('store.Datastore.motor.motor_asyncio')
	def test_insert_existing(self, motor_mock):
		song = MagicMock()
		song.id = 'kUaAszRmBbQ'

		mock_connection = { 'hummingbot': AsyncMock() }
		motor_mock.AsyncIOMotorClient.return_value = mock_connection

		datastore = Datastore()
		loop = asyncio.get_event_loop()
		loop.run_until_complete(datastore.insert_song(song))

		args, kwargs = mock_connection['hummingbot'].songs.find_one_and_update.call_args
		self.assertEqual(args, ({'videoId': 'kUaAszRmBbQ'}, {'$inc': { 'play_count': 1 } },))

	@patch('store.Datastore.motor.motor_asyncio')
	def test_update_song_skipped(self, motor_mock):
		song = MagicMock()
		song.id = 'kUaAszRmBbQ'

		mock_connection = { 'hummingbot': AsyncMock() }
		motor_mock.AsyncIOMotorClient.return_value = mock_connection

		datastore = Datastore()
		loop = asyncio.get_event_loop()
		loop.run_until_complete(datastore.update_song_skipped(song))

		args, kwargs = mock_connection['hummingbot'].songs.find_one_and_update.call_args
		self.assertEqual(args, ({'videoId': 'kUaAszRmBbQ'}, {'$inc': { 'skip_count': 1 } },))