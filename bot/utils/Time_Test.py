import unittest
from unittest.mock import patch, MagicMock

from utils.Timer import Timer
from utils.Timer import TimerError

class TimerTest(unittest.TestCase):

	@patch('utils.Timer.time')
	def test_initialization_default(self, time_mock):
		timer = Timer()

		self.assertEqual(timer.initial_start_time, 0)
		self.assertEqual(timer.start_time, 0)
		self.assertEqual(timer.pause_started, None)
		self.assertEqual(timer.amount_time_paused, 0)

	@patch('utils.Timer.time')
	def test_initialization_start_time(self, time_mock):
		timer = Timer(50)

		self.assertEqual(timer.initial_start_time, 50)
		self.assertEqual(timer.start_time, 0)
		self.assertEqual(timer.pause_started, None)
		self.assertEqual(timer.amount_time_paused, 0)

	@patch('utils.Timer.time')
	def test_start(self, time_mock):
		time_mock.time.return_value = 1525628158.745443

		timer = Timer()
		timer.start()

		self.assertEqual(timer.start_time, 1525628158)

	@patch('utils.Timer.time')
	def test_start_already_started(self, time_mock):
		time_mock.time.return_value = 1525628158.745443

		timer = Timer()
		timer.start()

		self.assertRaises(TimerError, timer.start)

	@patch('utils.Timer.time')
	def test_pause(self, time_mock):
		timer = Timer()

		time_mock.time.return_value = 1525628158.745443
		timer.start()

		time_mock.time.return_value = 1525628188.142346
		timer.pause()

		self.assertEqual(timer.pause_started, 1525628188)

	def test_pause_not_started(self):
		timer = Timer()
		
		self.assertRaises(TimerError, timer.pause)

	@patch('utils.Timer.time')
	def test_pause_already_paused(self, time_mock):
		time_mock.time.return_value = 1525628188.142346
		
		timer = Timer()
		timer.start()
		timer.pause()
		
		self.assertRaises(TimerError, timer.pause)

	@patch('utils.Timer.time')
	def test_resume(self, time_mock):
		timer = Timer()

		time_mock.time.return_value = 1525628158.745443
		timer.start()

		time_mock.time.return_value = 1525628188.142346
		timer.pause()

		time_mock.time.return_value = 1525628198.142346
		timer.resume()

		self.assertEqual(timer.amount_time_paused, 10)
		self.assertEqual(timer.pause_started, None)

	@patch('utils.Timer.time')
	def test_resume_not_paused(self, time_mock):
		timer = Timer()

		time_mock.time.return_value = 1525628158.745443
		timer.start()

		self.assertRaises(TimerError, timer.resume)

	def test_resume_not_started(self):
		timer = Timer()

		self.assertRaises(TimerError, timer.resume)

	@patch('utils.Timer.time')
	def test_get_elapsed_seconds(self, time_mock):
		timer = Timer()

		time_mock.time.return_value = 1525628158.745443
		timer.start()

		time_mock.time.return_value = 1525628188.142346
		self.assertEqual(timer.get_elapsed_seconds(), 30)

	@patch('utils.Timer.time')
	def test_get_elapsed_seconds_initial_start_time(self, time_mock):
		timer = Timer(20)

		time_mock.time.return_value = 1525628158.745443
		timer.start()

		time_mock.time.return_value = 1525628188.142346
		self.assertEqual(timer.get_elapsed_seconds(), 50)

	@patch('utils.Timer.time')
	def test_get_elapsed_seconds_paused(self, time_mock):
		timer = Timer()

		time_mock.time.return_value = 1525628158.745443
		timer.start()

		time_mock.time.return_value = 1525628188.142346
		timer.pause()

		time_mock.time.return_value = 1525628198.142346
		self.assertEqual(timer.get_elapsed_seconds(), 30)

	@patch('utils.Timer.time')
	def test_get_elapsed_seconds_with_pause(self, time_mock):
		timer = Timer()

		time_mock.time.return_value = 1525628158.745443
		timer.start()

		time_mock.time.return_value = 1525628188.142346
		timer.pause()

		time_mock.time.return_value = 1525628198.142346
		timer.resume()

		time_mock.time.return_value = 1525628208.142346
		self.assertEqual(timer.get_elapsed_seconds(), 40)

	def test_get_elapsed_seconds_not_started(self):
		timer = Timer()

		self.assertEqual(timer.get_elapsed_seconds(), 0)

	@patch('utils.Timer.time')
	def test_get_current_timestamp_not_started(self, time_mock):
		timer = Timer()

		self.assertEqual(timer.get_current_timestamp(), '00h:00m:00s')

	@patch('utils.Timer.time')
	def test_get_current_timestamp(self, time_mock):
		timer = Timer()

		time_mock.time.return_value = 1525628158.745443
		timer.start()

		time_mock.time.return_value = 1525664910.142346
		self.assertEqual(timer.get_current_timestamp(), '10h:12m:32s')
