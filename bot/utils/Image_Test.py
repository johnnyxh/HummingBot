import asyncio
import unittest
from unittest.mock import patch, MagicMock

from utils.Image import Image

class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)

class ImageTest(unittest.TestCase):

	def setUp(self):
		self.bot_mock = AsyncMock()
		self.message_mock = MagicMock()
		self.message_mock.channel = 'SomeChannel'

	def test_brazzers_invalid_image(self):
		image = Image(self.bot_mock)
		self.message_mock.content = '?image brazzers http://www.google.com'

		loop = asyncio.get_event_loop()
		loop.run_until_complete(image.brazzers(self.message_mock))

		args, kwargs = self.bot_mock.add_reaction.call_args
		self.assertEqual(args, (self.message_mock, '❌'))

		args, kwargs = self.bot_mock.send_message.call_args
		self.assertEqual(args, ('SomeChannel', 'Cannot identify image file'))

	def test_brazzers_valid_image(self):
		image = Image(self.bot_mock)
		self.message_mock.content = '?image brazzers http://via.placeholder.com/350x150'

		loop = asyncio.get_event_loop()
		loop.run_until_complete(image.brazzers(self.message_mock))

		self.assertTrue(self.bot_mock.send_file.called)
