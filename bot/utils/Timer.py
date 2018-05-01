import math
import time

class Timer:
	def __init__(self, intial_start_time = 0):
		self.intial_start_time = intial_start_time
		self.start_time = 0
		self.pause_started = None
		self.amount_time_paused = 0

	def start(self):
		self.start_time = math.floor(time.time())

	def pause(self):
		self.pause_started = math.floor(time.time())

	def resume(self):
		self.amount_time_paused += math.floor(time.time()-self.pause_started)
		self.pause_started = None

	def get_elapsed_seconds(self):
		# if the timer hasn't started
		if self.start_time == 0: return 0

		current_timestamp = math.floor(time.time() + self.intial_start_time)
		adjusted_start_time = self.start_time

		# account for when the timer is still in paused state
		if self.pause_started is not None: adjusted_start_time += math.floor(time.time()-self.pause_started)

		adjusted_start_time += self.amount_time_paused

		return current_timestamp-adjusted_start_time

	def get_current_timestamp(self):
		# if the timer hasn't started
		if self.start_time == 0: return "00h:00m:00.00s"
		
		hours, rem = divmod(self.get_elapsed_seconds(), 3600)
		minutes, seconds = divmod(rem, 60)
		return "{:0>2}h:{:0>2}m:{:0>2}s".format(int(hours),int(minutes),int(seconds))